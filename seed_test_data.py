# seed_test_data.py

import django
import os
from datetime import timedelta, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from gyms.models import Gym
from activities.models import ActivityCategory, ActivitySubcategory, Activity
from plans.models import Plan, PlanActivity
from clients.models import Client
from subscriptions.models import Subscription
from auth_app.models import CustomUser

# Crear usuario propietario
owner, _ = CustomUser.objects.get_or_create(
    email='admin@gymtest.com',
    defaults={
        'first_name': 'Admin',
        'last_name': 'Gym',
        'is_superuser': True,
        'is_staff': True
    }
)
owner.set_password('admin123')
owner.save()

# Crear gimnasio con owner
gym, _ = Gym.objects.get_or_create(name='Gym Test', owner=owner)

# Crear categorías y subcategorías
cat = ActivityCategory.objects.create(name='Clases Grupales', gym=gym)
subcat = ActivitySubcategory.objects.create(name='Yoga', category=cat)

# Crear actividad
activity = Activity.objects.create(
    name='Yoga 50min',
    gym=gym,
    category=cat,
    subcategory=subcat,
    description='Clase relajante de yoga',
    duration_minutes=50,
    intensity='medium',
    min_reservation_notice=timedelta(hours=24),
    min_cancellation_notice=timedelta(hours=4),
    is_active=True
)

# Crear plan
plan = Plan.objects.create(
    name='Plan Yoga Mensual',
    category='mensual',
    subcategory='fitness',
    plan_type='subscription',
    price=40,
    price_includes_tax=True,
    tax_percentage=21,
    billing_day=1,
    enable_prorate=True,
    auto_renew=True,
    is_active=True
)

PlanActivity.objects.create(
    plan=plan,
    activity=activity,
    limit_type='per_week',
    limit_quantity=3
)

# Crear cliente
client = Client.objects.create(first_name='Juan', last_name='Pérez', gym=gym)

# Crear suscripción
today = date.today()
sub = Subscription.objects.create(
    client=client,
    plan=plan,
    name='Yoga Mensual',
    start_date=today,
    end_date=today + timedelta(days=30),
    price=plan.price
)
sub.copy_plan_activities()

print('✅ Datos cargados correctamente.')
