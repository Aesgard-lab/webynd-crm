# backend/saas_payments/webhooks.py
import json
import logging
from datetime import datetime, timezone

import stripe
from django.conf import settings
from django.db import transaction
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from gyms.models import Gym
from saas.models import ModulePrice
from saas_payments.models import (
    GymStripeCustomer,
    GymStripeSubscription,
    GymStripeSubscriptionItem,
)

logger = logging.getLogger(__name__)


def _ts_to_dt(ts: int | None):
    if not ts:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def _find_gym_from_customer_id(customer_id: str) -> Gym | None:
    try:
        gsc = GymStripeCustomer.objects.select_related("gym").get(
            stripe_customer_id=customer_id
        )
        return gsc.gym
    except GymStripeCustomer.DoesNotExist:
        return None


@transaction.atomic
def _sync_subscription_from_stripe(sub_obj: dict):
    """
    Sincroniza GymStripeSubscription y GymStripeSubscriptionItem
    a partir de un objeto stripe.Subscription (expandido).
    """
    stripe_subscription_id = sub_obj["id"]
    customer_id = sub_obj["customer"]

    gym = _find_gym_from_customer_id(customer_id)
    if gym is None:
        # Como red de seguridad: si por alguna razón no existe el cliente,
        # no fallamos; solo registramos.
        logger.warning(
            "Stripe subscription %s con customer %s sin Gym asociado",
            stripe_subscription_id,
            customer_id,
        )
        return

    status = sub_obj["status"]  # trialing, active, past_due, canceled, unpaid, ...
    current_period_start = _ts_to_dt(sub_obj.get("current_period_start"))
    current_period_end = _ts_to_dt(sub_obj.get("current_period_end"))
    cancel_at_period_end = bool(sub_obj.get("cancel_at_period_end"))
    canceled_at = _ts_to_dt(sub_obj.get("canceled_at"))

    subscription, _created = GymStripeSubscription.objects.update_or_create(
        stripe_subscription_id=stripe_subscription_id,
        defaults=dict(
            gym=gym,
            status=status,
            current_period_start=current_period_start,
            current_period_end=current_period_end,
            cancel_at_period_end=cancel_at_period_end,
            canceled_at=canceled_at,
        ),
    )

    # Sincronizar items (mirror completo)
    live_price_ids = set()
    for item in sub_obj.get("items", {}).get("data", []):
        price = item["price"]
        stripe_price_id = price["id"]
        stripe_product_id = price.get("product")
        quantity = item.get("quantity", 1)

        live_price_ids.add(stripe_price_id)

        # Intentar enlazar con ModulePrice por stripe_price_id
        mp = ModulePrice.objects.filter(stripe_price_id=stripe_price_id).first()

        GymStripeSubscriptionItem.objects.update_or_create(
            subscription=subscription,
            stripe_price_id=stripe_price_id,
            defaults=dict(
                stripe_product_id=stripe_product_id,
                quantity=quantity,
                module_price=mp,
            ),
        )

    # Eliminar items que ya no existan en Stripe
    GymStripeSubscriptionItem.objects.filter(
        subscription=subscription
    ).exclude(stripe_price_id__in=live_price_ids).delete()

    logger.info(
        "SYNC OK: sub=%s gym=%s status=%s items=%d",
        stripe_subscription_id,
        gym.id,
        status,
        len(live_price_ids),
    )


class StripeWebhookView(APIView):
    """
    Webhook sin auth (Stripe firma).
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=sig_header,
                secret=endpoint_secret,
            )
        except ValueError:
            logger.exception("Webhook: payload inválido")
            return Response({"detail": "Invalid payload"}, status=400)
        except stripe.error.SignatureVerificationError:
            logger.exception("Webhook: firma inválida")
            return Response({"detail": "Invalid signature"}, status=400)

        event_type = event["type"]
        data_obj = event["data"]["object"]

        try:
            # Usamos un único camino de sync: recuperar la sub desde Stripe expandida.
            if event_type in (
                "checkout.session.completed",
                "customer.subscription.created",
                "customer.subscription.updated",
                "customer.subscription.deleted",
                "invoice.paid",
                "invoice.payment_failed",
            ):
                sub_id = None

                if event_type == "checkout.session.completed":
                    # Solo nos interesan sesiones de subscripción
                    if data_obj.get("mode") == "subscription":
                        sub_id = data_obj.get("subscription")
                        # Asegurar que el GymStripeCustomer exista
                        customer_id = data_obj.get("customer")
                        if customer_id and _find_gym_from_customer_id(customer_id) is None:
                            # Si quien inició checkout no había pasado por ensure_customer,
                            # intentamos enlazar por si existe en BD (opcional).
                            GymStripeCustomer.objects.get_or_create(
                                stripe_customer_id=customer_id,
                                defaults={"gym": None},  # ajusta si tu modelo requiere gym obligatorio
                            )

                elif event_type.startswith("customer.subscription."):
                    sub_id = data_obj.get("id")

                elif event_type.startswith("invoice."):
                    # invoice -> sub está en subscription
                    sub_id = data_obj.get("subscription")

                if sub_id:
                    # Recuperar sub con items expandido (unica fuente de verdad)
                    sub = stripe.Subscription.retrieve(
                        sub_id,
                        expand=["items.data.price.product"],
                    )
                    _sync_subscription_from_stripe(sub)

            else:
                logger.info("Webhook no manejado: %s", event_type)

        except Exception:
            logger.exception("Error procesando evento %s", event_type)
            return Response({"detail": "Error handling event"}, status=500)

        return Response({"received": True})
