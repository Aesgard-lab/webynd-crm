from .base import KPIBaseView

class InformacionesKPI(KPIBaseView):
    required_perm = "can_manage_clients"

    def get(self, request):
        data = {"count": 17, "period": {"from": "2025-08-01", "to": "2025-08-31"}}
        return self.ok(data)
