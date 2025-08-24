from .base import KPIBaseView

class KPIOverview(KPIBaseView):
    # required_perm = None
    def get(self, request):
        data = {
            "activeClients": 1860,
            "activeMemberships": 1209,
            "monthlyRevenue": 9340,
            "churnThisMonth": 3,
        }
        return self.ok(data)
