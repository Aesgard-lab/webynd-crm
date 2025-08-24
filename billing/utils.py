from .models import BillingEntry
from core.models import GymSettings


def create_billing_entry(gym, client, item_type, reference_id, concept, unit_price, quantity=1, tax_percentage=None):
    settings = gym.settings

    # Definir IVA
    tax = tax_percentage if tax_percentage is not None else settings.get_value('tax_percentage') or 21

    # Cálculos
    subtotal = unit_price * quantity
    total_iva = round(subtotal * (tax / 100), 2)
    total_price = round(subtotal + total_iva, 2)

    # Numeración
    prefix = settings.get_value('invoice_prefix') or "INV"
    number = settings.get_value('next_invoice_number') or 1
    invoice_number = f"{prefix}-{str(number).zfill(5)}"

    # Crear entrada
    entry = BillingEntry.objects.create(
        gym=gym,
        client=client,
        item_type=item_type,
        reference_id=reference_id,
        concept=concept,
        invoice_number=invoice_number,
        unit_price=unit_price,
        quantity=quantity,
        tax_percentage=tax,
        total_tax=total_iva,
        total_price=total_price,
        status='paid',
    )

    # Incrementar numeración
    settings.next_invoice_number = number + 1
    settings.save()

    return entry
