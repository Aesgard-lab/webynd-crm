# reports/services/riesgo_baja.py

from datetime import timedelta
from django.utils import timezone
from clients.models import Client
from subscriptions.models import Subscription
from bonuses.models import Bonus
from scheduler.models import Reservation
from django.db.models import Q


def detectar_clientes_en_riesgo(user, params):
    gym = getattr(user, 'gym', None)
    if not gym:
        return {"error": "Usuario sin gimnasio asignado."}

    # Umbrales con valores por defecto
    dias_inactivo = int(params.get("dias_inactivo", 14))
    dias_expira = int(params.get("dias_expira", 7))
    frecuencia_minima = int(params.get("frecuencia_minima", 2))

    fecha_actual = timezone.now().date()
    fecha_inicio_frecuencia = fecha_actual - timedelta(days=30)
    fecha_inactividad = fecha_actual - timedelta(days=dias_inactivo)

    clientes = Client.objects.filter(gym=gym)
    en_riesgo = []

    for cliente in clientes:
        razones = []

        # Asistencias en últimos 30 días
        asistencias = Reservation.objects.filter(
            client=cliente,
            cancelled=False,
            checked_in=True,
            session__start_time__date__gte=fecha_inicio_frecuencia,
            session__start_time__date__lte=fecha_actual
        )

        # Última asistencia
        ultima_asistencia = asistencias.order_by('-session__start_time').first()
        if not ultima_asistencia or ultima_asistencia.session.start_time.date() < fecha_inactividad:
            razones.append(f"No asiste desde hace más de {dias_inactivo} días")

        # Frecuencia semanal
        total_asistencias = asistencias.count()
        frecuencia = total_asistencias / 4  # 4 semanas
        if frecuencia < frecuencia_minima:
            razones.append(f"Frecuencia baja: {frecuencia:.2f}/semana")

        # Suscripción por expirar sin renovación
        subs_activas = Subscription.objects.filter(
            client=cliente,
            gym=gym,
            status='active',
            end_date__gte=fecha_actual
        ).order_by('end_date')

        if subs_activas.exists():
            end_date = subs_activas.first().end_date
            if (end_date - fecha_actual).days <= dias_expira:
                razones.append(f"Suscripción expira en { (end_date - fecha_actual).days } días")
        else:
            razones.append("Sin suscripción activa")

        # Comparar última compra con promedio anterior
        ultimas_subs = Subscription.objects.filter(client=cliente, gym=gym).order_by('-created_at')[:5]
        ultimos_bonos = Bonus.objects.filter(client=cliente, gym=gym).order_by('-created_at')[:5]

        compras = list(ultimas_subs) + list(ultimos_bonos)
        compras.sort(key=lambda c: c.created_at, reverse=True)

        if len(compras) >= 2:
            ultima = compras[0].price
            promedio_anterior = sum(c.price for c in compras[1:]) / (len(compras) - 1)
            if ultima < promedio_anterior:
                razones.append(f"Última compra más barata que el promedio anterior")

        # Si cumple alguna condición
        if razones:
            en_riesgo.append({
                "cliente_id": cliente.id,
                "nombre": cliente.full_name,
                "razones": razones,
            })

    return {
        "total_en_riesgo": len(en_riesgo),
        "clientes": en_riesgo
    }
