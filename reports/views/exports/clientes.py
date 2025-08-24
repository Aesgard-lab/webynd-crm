# reports/views/exports/clientes.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reports.services.clientes import generar_reporte_clientes


class ClienteReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filtros = request.query_params.dict()
        data = generar_reporte_clientes(request.user, filtros)

        if "error" in data:
            return Response(data, status=400)

        return Response(data)
