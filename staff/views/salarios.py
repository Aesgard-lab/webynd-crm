from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from staff.services.salarios import calcular_salario_mensual
from staff.models import Staff


class StaffSalaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, staff_id):
        try:
            staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            return Response({"error": "Staff no encontrado"}, status=404)

        mes = int(request.GET.get("mes", 8))
        año = int(request.GET.get("año", 2025))

        data = calcular_salario_mensual(staff_id, mes, año)
        return Response(data)
