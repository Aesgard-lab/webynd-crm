# reports/services/facturacion.py

from billing.models import BillingEntry, Expense
from django.db.models import Sum
from subscriptions.models import Subscription
from bonuses.models import Bonus
from django.utils import timezone

def calcular_facturacion(gym, start_date=None, end_date=None):
    ingresos_qs = BillingEntry.objects.filter(gym=gym)
    gastos_qs = Expense.objects.filter(gym=gym)

    if start_date:
        ingresos_qs = ingresos_qs.filter(created_at__date__gte=start_date)
        gastos_qs = gastos_qs.filter(date__gte=start_date)

    if end_date:
        ingresos_qs = ingresos_qs.filter(created_at__date__lte=end_date)
        gastos_qs = gastos_qs.filter(date__lte=end_date)

    total_ingresos = ingresos_qs.aggregate(total=Sum('total_price'))['total'] or 0
    total_gastos = gastos_qs.aggregate(total=Sum('amount'))['total'] or 0

    return {
        'ingresos': total_ingresos,
        'gastos': total_gastos,
        'balance': total_ingresos - total_gastos,
        
    }

def generar_reporte_financiero(user, start_date=None, end_date=None):
    gym = getattr(user, 'gym', None)
    if not gym:
        return {"error": "Usuario sin gimnasio asignado."}

    billing_qs = BillingEntry.objects.filter(gym=gym)
    expense_qs = Expense.objects.filter(gym=gym)

    if start_date:
        billing_qs = billing_qs.filter(created_at__date__gte=start_date)
        expense_qs = expense_qs.filter(date__gte=start_date)
    if end_date:
        billing_qs = billing_qs.filter(created_at__date__lte=end_date)
        expense_qs = expense_qs.filter(date__lte=end_date)

    ingresos_totales = billing_qs.aggregate(total=Sum('total_price'))['total'] or 0
    gastos_totales = expense_qs.aggregate(total=Sum('amount'))['total'] or 0

    clientes_unicos = billing_qs.values('client').distinct().count()
    ticket_medio = ingresos_totales / clientes_unicos if clientes_unicos > 0 else 0

    today = timezone.now().date()
    future_subs = Subscription.objects.filter(gym=gym, status='active', end_date__gte=today)
    future_bonuses = Bonus.objects.filter(gym=gym, remaining_uses__gt=0, expiration_date__gte=today)

    facturacion_futura_subs = future_subs.aggregate(total=Sum('price'))['total'] or 0
    facturacion_futura_bonuses = future_bonuses.aggregate(total=Sum('price'))['total'] or 0
    facturacion_futura = facturacion_futura_subs + facturacion_futura_bonuses

    return {
        "ingresos_totales": round(ingresos_totales, 2),
        "gastos_totales": round(gastos_totales, 2),
        "balance_neto": round(ingresos_totales - gastos_totales, 2),
        "clientes_unicos": clientes_unicos,
        "ticket_medio": round(ticket_medio, 2),
        "facturacion_futura_estimada": round(facturacion_futura, 2),
    }
