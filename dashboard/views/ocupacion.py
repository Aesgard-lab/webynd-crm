from .base import KPIBaseView

class OcupacionKPI(KPIBaseView):
    required_perm = "can_manage_activities"

    def get(self, request):
        data = {
            "today": [
                {"hour": "08:00", "capacity": 88, "booked": 75},
                {"hour": "09:30", "capacity": 90, "booked": 90},
                {"hour": "11:00", "capacity": 88, "booked": 60},
                {"hour": "12:30", "capacity": 88, "booked": 85},
                {"hour": "14:00", "capacity": 88, "booked": 70},
            ]
        }
        return self.ok(data)
