from .base import KPIBaseView

class FacturacionKPI(KPIBaseView):
    required_perm = "can_manage_cash"

    def get(self, request):
        totals = [8200, 6400, 7100, 6600, 9100, 10200, 4400]
        m = max(totals) or 1
        bars = [round(v / m, 3) for v in totals]
        labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul"]

        data = {"totals": totals, "bars": bars, "labels": labels, "currency": "EUR"}
        return self.ok(data)
