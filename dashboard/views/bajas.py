from .base import KPIBaseView

class BajasKPI(KPIBaseView):
    required_perm = "can_manage_clients"

    def get(self, request):
        data = {"count": 3, "period": {"from": "2025-08-01", "to": "2025-08-31"}}
        return self.ok(data)
