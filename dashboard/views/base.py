from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from dashboard.permissions import CanViewKPI

class KPIBaseView(APIView):
    permission_classes = [IsAuthenticated, CanViewKPI]
    required_perm = None  # las subclases pueden sobrescribirla

    def ok(self, data, status=200):
        return Response(data, status=status)
