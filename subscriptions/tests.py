from django.test import TestCase
from .models import Subscription
from clients.models import Client
from datetime import date, timedelta

class SubscriptionTests(TestCase):
    def setUp(self):
        self.client1 = Client.objects.create(first_name='Juan', last_name='Pérez')

    def test_fecha_invalida(self):
        start = date.today()
        end = start - timedelta(days=1)
        with self.assertRaises(Exception):
            Subscription.objects.create(client=self.client1, name="Test", start_date=start, end_date=end)

    def test_unica_activa(self):
        today = date.today()
        Subscription.objects.create(client=self.client1, name="Activa", start_date=today, end_date=today + timedelta(days=10))
        with self.assertRaises(Exception):
            Subscription.objects.create(client=self.client1, name="Segunda", start_date=today, end_date=today + timedelta(days=5))

