# saas_payments/stripe_service.py
from typing import Iterable, List
import stripe
from django.conf import settings
from django.db import transaction
from django.utils.text import slugify

from gyms.models import Gym
from saas.models import Module, ModulePrice, PriceCycle
from .models import GymStripeCustomer

stripe.api_key = settings.STRIPE_SECRET_KEY

CYCLE_MAP = {
    PriceCycle.MONTHLY: ("month", 1),
    PriceCycle.QUARTERLY: ("month", 3),
    PriceCycle.ANNUAL: ("year", 1),
}

def ensure_customer(gym: Gym) -> GymStripeCustomer:
    customer = getattr(gym, "stripe_customer", None)
    if customer and customer.stripe_customer_id:
        return customer

    email = getattr(gym.owner, "email", None) or ""
    name = f"{gym.name} ({gym.owner.email if gym.owner else ''})".strip()

    # crea local si no existe
    customer = customer or GymStripeCustomer.objects.create(
        gym=gym, billing_email=email
    )

    # crea en Stripe si no hay id
    if not customer.stripe_customer_id:
        sc = stripe.Customer.create(email=email or None, name=name or None, metadata={"gym_id": str(gym.id)})
        customer.stripe_customer_id = sc["id"]
        customer.save(update_fields=["stripe_customer_id"])
    return customer


@transaction.atomic
def ensure_product(module: Module) -> Module:
    if module.stripe_product_id:
        return module
    sp = stripe.Product.create(name=module.name, description=(module.description or ""), metadata={"module_id": str(module.id), "code": module.code})
    module.stripe_product_id = sp["id"]
    module.save(update_fields=["stripe_product_id"])
    return module


@transaction.atomic
def ensure_price(mp: ModulePrice) -> ModulePrice:
    if mp.stripe_price_id:
        return mp
    # asegúrate de tener el product
    ensure_product(mp.module)
    interval, interval_count = CYCLE_MAP[mp.cycle]
    sp = stripe.Price.create(
        currency=mp.currency.lower(),
        unit_amount=int(mp.amount * 100),
        product=mp.module.stripe_product_id,
        recurring={"interval": interval, "interval_count": interval_count},
        metadata={"module_price_id": str(mp.id), "module_id": str(mp.module_id), "cycle": mp.cycle},
    )
    mp.stripe_price_id = sp["id"]
    mp.save(update_fields=["stripe_price_id"])
    return mp


def create_checkout_session(*, gym: Gym, module_price_ids: Iterable[int], success_url: str | None = None, cancel_url: str | None = None) -> str:
    """
    Devuelve la URL de Checkout (modo subscription) para que el gimnasio añada su tarjeta y empiece la suscripción.
    Sin prorrateo en cambios futuros (lo controlaremos por API).
    """
    # 1) customer
    customer = ensure_customer(gym)

    # 2) prices
    mps: List[ModulePrice] = list(ModulePrice.objects.filter(id__in=list(module_price_ids)))
    if not mps:
        raise ValueError("No se han encontrado ModulePrice válidos.")

    for mp in mps:
        ensure_price(mp)

    line_items = [{"price": mp.stripe_price_id, "quantity": 1} for mp in mps]

    # 3) checkout session (subscription)
    session = stripe.checkout.Session.create(
        mode="subscription",
        customer=customer.stripe_customer_id,
        line_items=line_items,
        success_url=(success_url or settings.STRIPE_SUCCESS_URL),
        cancel_url=(cancel_url or settings.STRIPE_CANCEL_URL),
        allow_promotion_codes=False,
        subscription_data={
            # importante para tu caso: sin prorrateo en cambios posteriores
            "proration_behavior": "none",
            "metadata": {"gym_id": str(gym.id)},
        },
        metadata={"gym_id": str(gym.id)},
        # opcional: automatic_tax={"enabled": False},
    )
    return session["url"]


def create_billing_portal_session(*, gym: Gym, return_url: str | None = None) -> str:
    customer = ensure_customer(gym)
    portal = stripe.billing_portal.Session.create(
        customer=customer.stripe_customer_id,
        return_url=(return_url or settings.STRIPE_PORTAL_RETURN_URL),
    )
    return portal["url"]
