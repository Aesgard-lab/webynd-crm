# reports/services/exportador_csv.py

import csv
from django.http import HttpResponse


def exportar_csv_financiero(data_dict: dict) -> HttpResponse:
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_financiero.csv"'

    writer = csv.writer(response)
    writer.writerow(['KPI', 'Valor'])

    for kpi, valor in data_dict.items():
        writer.writerow([kpi, valor])

    return response
