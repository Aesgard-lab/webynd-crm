from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from auth_app.models import CustomUser
from gyms.models import Gym
from staff.models import Staff
from clients.models import Client
from activities.models import Activity
from scheduler.models import ScheduledSession, Reservation

class SchedulerTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()

        # Crear usuario admin
        self.admin = CustomUser.objects.create_user(
            email="admin@gym.com", password="admin123", is_admin=True
        )

        # Crear gimnasio
        self.gym = Gym.objects.create(name="Test Gym", owner=self.admin)

        # Crear actividad
        self.activity = Activity.objects.create(
            name="Yoga",
            description="Clase de yoga",
            duration_minutes=60,
            intensity="low",
            gym=self.gym,
            min_reservation_notice=timedelta(hours=1),
            min_cancellation_notice=timedelta(hours=2)
        )

        # Crear staff
        self.staff_user = CustomUser.objects.create_user(email="staff@gym.com", password="staff123")
        self.staff = Staff.objects.create(
            user=self.staff_user,
            first_name="John", last_name="Doe", email="staff@gym.com",
            gym=self.gym, can_sell=True
        )

        # Crear cliente
        self.client_user = CustomUser.objects.create_user(email="cliente@gym.com", password="client123")
        self.client_model = Client.objects.create(user=self.client_user, gym=self.gym)

        # Autenticar como admin
        self.client_api.force_authenticate(user=self.admin)

    def test_create_session(self):
        url = reverse("sessions-list")
        data = {
            "gym": self.gym.id,
            "activity": self.activity.id,
            "start_time": (timezone.now() + timedelta(days=1)).isoformat(),
            "end_time": (timezone.now() + timedelta(days=1, hours=1)).isoformat(),
            "max_capacity": 10,
            "staff": [self.staff.id],
        }
        response = self.client_api.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ScheduledSession.objects.count(), 1)

    def test_create_reservation(self):
        # Crear sesión primero
        session = ScheduledSession.objects.create(
            gym=self.gym,
            activity=self.activity,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1),
            max_capacity=5
        )
        session.staff.add(self.staff)

        url = reverse("reservations-list")
        data = {
            "session": session.id,
            "client": self.client_model.id
        }
        response = self.client_api.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Reservation.objects.count(), 1)
