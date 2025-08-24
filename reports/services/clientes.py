# reports/services/clientes.py

from clients.models import Client
from subscriptions.models import Subscription
from django.db.models import Avg, Sum
from datetime import date


def generar_reporte_clientes(user, filtros: dict = None):
    gym = getattr(user, 'gym', None)
    if not gym:
        return {"error": "Usuario sin gimnasio asignado."}

    filtros = filtros or {}
    qs = Client.objects.filter(gym=gym)

    # 🎯 Aplicar filtros (alta, baja, edad, género, plan, estado, etc.)
    if 'estado' in filtros:
        qs = qs.filter(status=filtros['estado'])  # ejemplo: activo, baja, etc.
    if 'genero' in filtros:
        qs = qs.filter(gender=filtros['genero'])
    if 'plan_id' in filtros:
        qs = qs.filter(subscription__plan_id=filtros['plan_id'])

    clientes_data = []
    for cliente in qs:
        subs = Subscription.objects.filter(client=cliente, gym=gym)
        if not subs.exists():
            continue

        fecha_primera = subs.order_by('start_date').first().start_date
        fecha_ultima = subs.order_by('-end_date').first().end_date
        tiempo_total = (fecha_ultima - fecha_primera).days
        vida_media = round(tiempo_total / subs.count(), 1) if subs.count() > 0 else 0

        cltv = subs.aggregate(total=Sum('price'))['total'] or 0

        clientes_data.append({
            'id': cliente.id,
            'nombre': cliente.full_name,
            'genero': cliente.gender,
            'fecha_registro': cliente.created_at.date() if cliente.created_at else None,
            'vida_media': vida_media,
            'cltv': round(cltv, 2)
        })

    # KPIs globales
    vida_media_global = round(sum(c['vida_media'] for c in clientes_data) / len(clientes_data), 1) if clientes_data else 0
    cltv_promedio = round(sum(c['cltv'] for c in clientes_data) / len(clientes_data), 2) if clientes_data else 0

    return {
        'kpis': {
            'vida_media_global': vida_media_global,
            'cltv_promedio': cltv_promedio,
            'total_clientes': len(clientes_data),
        },
        'clientes': clientes_data
    }
