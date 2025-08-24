# dashboard/urls.py
from django.urls import path
from dashboard.views.altas import AltasKPI
from dashboard.views.bajas import BajasKPI
from dashboard.views.informaciones import InformacionesKPI
from dashboard.views.excedencias import ExcedenciasKPI
from dashboard.views.facturacion import FacturacionKPI
from dashboard.views.ocupacion import OcupacionKPI
from dashboard.views.overview import KPIOverview

urlpatterns = [
    # Resumen para el dashboard
    path("kpi/overview/", KPIOverview.as_view(), name="kpi-overview"),

    # KPIs operativas
    path("kpi/altas/", AltasKPI.as_view(), name="kpi-altas"),
    path("kpi/bajas/", BajasKPI.as_view(), name="kpi-bajas"),
    path("kpi/informaciones/", InformacionesKPI.as_view(), name="kpi-informaciones"),
    path("kpi/excedencias/", ExcedenciasKPI.as_view(), name="kpi-excedencias"),

    # KPIs de negocio / actividad
    path("kpi/facturacion/", FacturacionKPI.as_view(), name="kpi-facturacion"),
    path("kpi/ocupacion/", OcupacionKPI.as_view(), name="kpi-ocupacion"),
]
