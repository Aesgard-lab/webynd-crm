# activities/tests.py

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, time
from gyms.models import Gym
from .models import Activity, ActivityCategory, ActivitySubcategory

class ActivityModelTests(TestCase):
    def setUp(self):
        self.gym = Gym.objects.create(name="Gimnasio Test")
        self.category = ActivityCategory.objects.create(name="Clases Grupales", gym=self.gym)
        self.subcategory = ActivitySubcategory.objects.create(name="Yoga", category=self.category)

    def test_crear_actividad_basica(self):
        actividad = Activity.objects.create(
            name="Yoga 50min",
            gym=self.gym,
            category=self.category,
            subcategory=self.subcategory,
            description="Clase de yoga",
            duration_minutes=50,
            intensity='medium',
            min_reservation_notice=timedelta(hours=24),
            min_cancellation_notice=timedelta(hours=4),
            open_reservation_hour=time(hour=0, minute=0),
            is_active=True,
        )

        self.assertEqual(actividad.duration_minutes, 50)
        self.assertEqual(actividad.intensity, 'medium')
        self.assertTrue(actividad.is_active)
        self.assertEqual(actividad.category.name, "Clases Grupales")
        self.assertEqual(actividad.subcategory.name, "Yoga")

    def test_actividad_sin_hora_reserva_es_valida(self):
        actividad = Activity.objects.create(
            name="Crossfit",
            gym=self.gym,
            category=self.category,
            subcategory=self.subcategory,
            duration_minutes=45,
            intensity='high',
            min_reservation_notice=timedelta(hours=1),
            min_cancellation_notice=timedelta(hours=2),
            open_reservation_hour=None,
            is_active=True,
        )
        self.assertIsNone(actividad.open_reservation_hour)