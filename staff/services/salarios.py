# staff/services/salarios.py

from datetime import datetime, timedelta
from calendar import monthrange

from staff.models import Staff, SalaryRule
from scheduler.models import Reservation
from billing.models import BillingEntry
from services.models import Service
from activities.models import Activity
from django.db.models import Sum

from django.utils.timezone import make_aware


def calcular_salario_mensual(staff_id, mes, año):
    staff = Staff.objects.get(id=staff_id)
    reglas = staff.salary_rules.filter(activo=True)

    # Rango de fechas
    fecha_inicio = make_aware(datetime(año, mes, 1))
    fecha_fin = make_aware(datetime(año, mes, monthrange(año, mes)[1], 23, 59, 59))

    total = 0
    detalle = []

    for regla in reglas:
        monto = 0
        if regla.tipo_regla == 'fixed_monthly':
            monto = float(regla.valor)

        elif regla.tipo_regla == 'per_class':
            monto = calcular_pago_por_clases(staff, regla, fecha_inicio, fecha_fin)

        elif regla.tipo_regla == 'per_service':
            monto = calcular_pago_por_servicios(staff, regla, fecha_inicio, fecha_fin)

        elif regla.tipo_regla == 'per_sale':
            monto = calcular_comision_ventas(staff, regla, fecha_inicio, fecha_fin)

        total += monto
        detalle.append({
            'regla': str(regla),
            'monto': round(monto, 2),
        })

    return {
        'staff': staff.id,
        'nombre': f"{staff.first_name} {staff.last_name}",
        'mes': mes,
        'año': año,
        'total': round(total, 2),
        'detalle': detalle
    }

def calcular_pago_por_clases(staff, regla, inicio, fin):
    sesiones = staff.scheduled_sessions.filter(
        start_time__range=(inicio, fin),
        is_active=True
    )

    if regla.actividad:
        sesiones = sesiones.filter(activity=regla.actividad)

    if regla.hora_inicio and regla.hora_fin:
        sesiones = sesiones.filter(
            start_time__time__gte=regla.hora_inicio,
            start_time__time__lte=regla.hora_fin
        )

    total = 0
    for sesion in sesiones:
        if regla.por_cliente_asistido:
            asistentes = sesion.reservations.filter(cancelled=False, checked_in=True).count()
            valor = float(regla.valor) * asistentes
        else:
            valor = float(regla.valor)

        if regla.modo_pago == 'percent':
            # Supón que el valor base es 10€/clase (ajustable)
            valor = (10 * valor / 100)

        total += valor

    return total


def calcular_pago_por_servicios(staff, regla, inicio, fin):
    sesiones = staff.scheduled_sessions.filter(
        start_time__range=(inicio, fin),
        is_active=True,
        service__isnull=False
    )

    if regla.hora_inicio and regla.hora_fin:
        sesiones = sesiones.filter(
            start_time__time__gte=regla.hora_inicio,
            start_time__time__lte=regla.hora_fin
        )

    total = 0
    for sesion in sesiones:
        reservas = sesion.reservations.filter(cancelled=False)
        for r in reservas:
            if regla.por_cliente_asistido and not r.checked_in:
                continue
            precio = r.bonus_used.price if r.bonus_used else 20  # ← Estimar base si no hay bonus
            pago = float(regla.valor)
            if regla.modo_pago == 'percent':
                pago = precio * pago / 100
            total += pago

    return total

def calcular_comision_ventas(staff, regla, inicio, fin):
    ventas = BillingEntry.objects.filter(
        created_by=staff.user,
        created_at__range=(inicio, fin),
        gym=staff.gym
    )

    monto_total = ventas.aggregate(total=Sum('total_price'))['total'] or 0

    if regla.modo_pago == 'percent':
        return monto_total * float(regla.valor) / 100
    return float(regla.valor) * ventas.count()
