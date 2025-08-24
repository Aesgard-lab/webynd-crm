from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reports.services.riesgo_baja import detectar_clientes_en_riesgo


class RiesgoBajaReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Extrae parámetros desde querystring (ej: ?dias_inactivo=10)
        filtros = request.query_params.dict()
        resultado = detectar_clientes_en_riesgo(request.user, filtros)

        if "error" in resultado:
            return Response(resultado, status=400)

        return Response(resultado)
