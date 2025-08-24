import os
from celery import Celery

# ✔️ Cambiado al nombre correcto del módulo de configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('webynd_crm')  # este nombre es libre, puede quedar así
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
