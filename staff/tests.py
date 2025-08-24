from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from auth_app.models import CustomUser
from gyms.models import Gym
from staff.models import Staff


class TestStaff(TestCase):
    def setUp(self):
        self.client_api = APIClient()

        # Usuario admin
        self.admin = CustomUser.objects.create_user(
            email="admin@test.com", password="admin123", is_admin=True
        )

        # Gimnasio
        self.gym = Gym.objects.create(name="Gym Test", owner=self.admin)

        # Autenticación
        self.client_api.force_authenticate(user=self.admin)

    def test_create_staff_model(self):
        staff_user = CustomUser.objects.create_user(
            email="staff@test.com", password="staff123"
        )
        staff = Staff.objects.create(
            user=staff_user,
            first_name="John",
            last_name="Doe",
            email="staff@test.com",
            dni="12345678X",
            gym=self.gym,
            can_sell=True,
            can_create_subs=False,
        )
        self.assertEqual(str(staff), "John Doe (staff@test.com)")
        self.assertEqual(staff.gym, self.gym)
        self.assertTrue(staff.can_sell)

    def test_create_staff_via_api(self):
        url = reverse("staff-list")
        data = {
            "first_name": "Ana",
            "last_name": "Gómez",
            "email": "ana@gym.com",
            "dni": "87654321X",
            "gym": self.gym.id,
            "can_sell": True,
            "can_create_subs": True,
            "active": True
        }
        response = self.client_api.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Staff.objects.count(), 1)
        self.assertEqual(Staff.objects.first().email, "ana@gym.com")
