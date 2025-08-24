# reports/views/export/financieros.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from billing.models import BillingEntry, Expense
from subscriptions.models import Subscription
from bonuses.models import Bonus

from django.utils import timezone
from django.db.models import Sum
from datetime import datetime
from rest_framework.views import APIView
from django.http import HttpResponse
from reports.services.facturacion import generar_reporte_financiero
from reports.services.exportador_csv import exportar_csv_financiero


class FinancialReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 🔐 Validación: asegurar que el usuario tiene gimnasio asignado
        gym = getattr(user, 'gym', None)
        if not gym:
            return Response({"error": "Usuario sin gimnasio asignado."}, status=400)

        # 📆 Filtros por fecha
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
        except ValueError:
            return Response({"error": "Formato de fecha inválido (YYYY-MM-DD)"}, status=400)

        # 🔍 QuerySets filtrados
        billing_qs = BillingEntry.objects.filter(gym=gym)
        expense_qs = Expense.objects.filter(gym=gym)

        if start_date:
            billing_qs = billing_qs.filter(created_at__date__gte=start_date)
            expense_qs = expense_qs.filter(date__gte=start_date)
        if end_date:
            billing_qs = billing_qs.filter(created_at__date__lte=end_date)
            expense_qs = expense_qs.filter(date__lte=end_date)

        # 📊 Ingresos
        ingresos_totales = billing_qs.aggregate(total=Sum('total_price'))['total'] or 0

        # 📉 Gastos
        gastos_totales = expense_qs.aggregate(total=Sum('amount'))['total'] or 0

        # 👥 Clientes únicos
        clientes_unicos = billing_qs.values('client').distinct().count()
        ticket_medio = ingresos_totales / clientes_unicos if clientes_unicos > 0 else 0

        # 🔮 Facturación futura estimada
        today = timezone.now().date()

        future_subs = Subscription.objects.filter(
            gym=gym,
            status='active',
            end_date__gte=today
        )
        future_bonuses = Bonus.objects.filter(
            gym=gym,
            remaining_uses__gt=0,
            expiration_date__gte=today
        )

        facturacion_futura_subs = future_subs.aggregate(total=Sum('price'))['total'] or 0
        facturacion_futura_bonuses = future_bonuses.aggregate(total=Sum('price'))['total'] or 0
        facturacion_futura = facturacion_futura_subs + facturacion_futura_bonuses

        # 📦 Respuesta final
        return Response({
            "ingresos_totales": round(ingresos_totales, 2),
            "gastos_totales": round(gastos_totales, 2),
            "balance_neto": round(ingresos_totales - gastos_totales, 2),
            "clientes_unicos": clientes_unicos,
            "ticket_medio": round(ticket_medio, 2),
            "facturacion_futura_estimada": round(facturacion_futura, 2),
            "rango_fecha": {
                "inicio": start_date_str,
                "fin": end_date_str
            }
        })


class FinancialReportCSVExportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # fechas
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
        except ValueError:
            return HttpResponse("Formato de fecha inválido (YYYY-MM-DD)", status=400)

        # calcular KPIs
        data = generar_reporte_financiero(user, start_date, end_date)
        if "error" in data:
            return HttpResponse(data["error"], status=400)

        # generar CSV
        return exportar_csv_financiero(data)
