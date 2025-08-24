from .base import KPIBaseView

class AltasKPI(KPIBaseView):
    required_perm = "can_manage_clients"

    def get(self, request):
        # Si más adelante quieres separar la lógica, crea una función aquí mismo
        # o en un módulo utils (NO en dashboard.views.kpis.*).
        data = {"count": 42, "period": {"from": "2025-08-01", "to": "2025-08-31"}}
        return self.ok(data)
