from django.test import TestCase, Client as TestClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from organizations.models import Gym
from clients.models import Client
from products.models import Product, ProductCategory
from sales.models import Order, OrderItem, OrderPayment
from finance.models import PaymentMethod
import json
from decimal import Decimal

User = get_user_model()

class SalesAPITest(TestCase):
    def setUp(self):
        # Setup Gym & User
        self.gym = Gym.objects.create(name="Test Gym")
        self.user = User.objects.create_user(username="staff", password="password")
        self.user.gym = self.gym # Assuming middleware or property handles this
        # If user.gym is a ManyToMany or uses 'profile', we might need to adjust.
        # But based on code 'request.gym = request.user.gym', it seems direct.
        # Wait, usually Middleware sets request.gym. 
        # API decorators use request.gym. We need to ensure request.gym is set or mocked.
        # If we use Client(), the middleware 'accounts.middleware.GymMiddleware' (guessing) might serve it.
        # Let's assume we need to login.
        self.client = TestClient()
        self.client.login(username="staff", password="password")
        
        # NOTE: If we need a Gym session/cookie/domain to trigger middleware, we might need more setup.
        # For now, let's try to patch request.gym or ensure the user->gym relation is correct.
        # If 'request.gym' comes from 'request.user.gym', we just need to set it.
        self.user.gyms.add(self.gym) # Assuming mechanism
        self.user.save()
        
        # Define a way to force gym context if middleware relies on it
        session = self.client.session
        session['current_gym_id'] = self.gym.id
        session.save()

        # Setup Data
        self.client_obj = Client.objects.create(gym=self.gym, first_name="John", last_name="Doe", email="john@example.com")
        self.category = ProductCategory.objects.create(gym=self.gym, name="General")
        self.product = Product.objects.create(
            gym=self.gym, name="Protein Shake", 
            base_price=10.00, tax_rate=None, category=self.category,
            stock=100
        )
        self.pm_cash = PaymentMethod.objects.create(gym=self.gym, name="Efectivo", is_active=True)
        self.pm_card = PaymentMethod.objects.create(gym=self.gym, name="Tarjeta", is_active=True)

    def test_process_sale_and_invoice(self):
        # 1. Process Sale
        url = reverse('api_pos_process_sale')
        data = {
            'client_id': self.client_obj.id,
            'items': [
                {'id': self.product.id, 'type': 'product', 'qty': 2, 'discount': {'value': 0}}
            ],
            'payments': [
                {'method_id': self.pm_cash.id, 'amount': 20.00}
            ],
            'action': 'NONE'
        }
        
        # Hack: Valid permission check might fail if not fully setup.
        # We assume @require_gym_permission decorator works if user has perms.
        # Grant perms?
        # from django.contrib.auth.models import Permission
        # p = Permission.objects.get(codename='add_sale')
        # self.user.user_permissions.add(p)
        
        # Testing middleware behavior manually might be hard. 
        # We'll just run it.
        
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.auth.models import Permission
        ct = ContentType.objects.get_for_model(Order)
        perm = Permission.objects.get(content_type=ct, codename='add_sale')
        self.user.user_permissions.add(perm)
        perm_view = Permission.objects.get(content_type=ct, codename='view_sale')
        self.user.user_permissions.add(perm_view)
        perm_change = Permission.objects.get(content_type=ct, codename='change_sale')
        self.user.user_permissions.add(perm_change)
        perm_delete = Permission.objects.get(content_type=ct, codename='delete_sale')
        self.user.user_permissions.add(perm_delete)
        self.user.save()

        try:
            response = self.client.post(url, data=json.dumps(data), content_type='application/json')
            
            if response.status_code != 200:
                print(f"RESPONSE ERROR: {response.content}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e
            
        self.assertEqual(response.status_code, 200)
        order_id = response.json()['order_id']
        
        order = Order.objects.get(id=order_id)
        self.assertEqual(order.total_amount, 20.00)
        self.assertEqual(order.status, 'PAID')
        
        # 2. Generate Invoice
        url_inv = reverse('api_order_generate_invoice', args=[order_id])
        res_inv = self.client.post(url_inv, data=json.dumps({'email': 'test@test.com'}), content_type='application/json')
        self.assertEqual(res_inv.status_code, 200)
        
        order.refresh_from_db()
        self.assertTrue(order.invoice_number.startswith('INV-'))
        
        # 3. Edit Order (Change Payment)
        url_upd = reverse('api_order_update', args=[order_id])
        update_data = {
            'payments': [
                {'method_id': self.pm_card.id, 'amount': 20.00}
            ]
        }
        res_upd = self.client.post(url_upd, data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(res_upd.status_code, 200)
        
        order.refresh_from_db()
        self.assertEqual(order.payments.first().payment_method, self.pm_card)
        
        # 4. Cancel Order
        url_cancel = reverse('api_order_cancel', args=[order_id])
        res_cancel = self.client.post(url_cancel)
        self.assertEqual(res_cancel.status_code, 200)
        
        order.refresh_from_db()
        self.assertEqual(order.status, 'CANCELLED')
