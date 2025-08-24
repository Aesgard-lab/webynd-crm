# reports/urls.py

from django.urls import path
from reports.views.exports.financieros import FinancialReportView, FinancialReportCSVExportView
from reports.views.exports.clientes import ClienteReportView
from reports.views.exports.riesgo_baja import RiesgoBajaReportView


urlpatterns = [
    path('financieros/', FinancialReportView.as_view(), name='financial-report'),
    path('financieros/export/csv/', FinancialReportCSVExportView.as_view(), name='financial-report-csv'),
    path('clientes/', ClienteReportView.as_view(), name='cliente-report'),
    path('clientes/riesgo_baja/', RiesgoBajaReportView.as_view(), name='reporte-riesgo-baja'),
]



