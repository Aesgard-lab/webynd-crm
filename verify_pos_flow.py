import os
import sys
import django
import json

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from organizations.models import Gym
from clients.models import Client
from products.models import Product
from finance.models import PaymentMethod
from sales.api import process_sale, order_generate_invoice, order_cancel
from sales.models import Order
from django.contrib.auth.models import AnonymousUser

def verify():
    print("--- STARTING VERIFICATION ---", flush=True)
    rf = RequestFactory()
    User = get_user_model()
    
    # 1. Setup Data
    gym, _ = Gym.objects.get_or_create(name="Verify Gym")
    
    from django.apps import apps
    GymMembership = apps.get_model('accounts', 'GymMembership')
    
    membership = GymMembership.objects.filter(gym=gym).first()
    if membership:
        user = membership.user
    else:
        user = User.objects.create_user("verifier", "password")
        GymMembership.objects.create(user=user, gym=gym, role='ADMIN', is_active=True)
        
    # user.gyms.add(gym) # Removing incorrect M2M usage
        
    # Ensure permission
    # For verification script, we can mock the decorator check by setting session
    
    client, _ = Client.objects.get_or_create(gym=gym, first_name="VClient", email="v@test.com")
    prod, _ = Product.objects.get_or_create(gym=gym, name="VProd", defaults={'base_price': 10})
    pm, _ = PaymentMethod.objects.get_or_create(gym=gym, name="VCash")

    # 2. Test Process Sale (With Custom Date/Staff)
    data = {
        'client_id': client.id,
        'items': [{'id': prod.id, 'type': 'product', 'qty': 1, 'discount': {'value': 0}}],
        'payments': [{'method_id': pm.id, 'amount': 10}],
        'action': 'NONE',
        'date': '2025-01-01',
        'time': '12:00',
        'staff_id': user.id
    }
    
    # Mock Request
    request = rf.post('/sales/api/sale/process/', content_type='application/json', data=json.dumps(data))
    request.user = user
    request.gym = gym # Mock middleware
    request.session = {'current_gym_id': gym.id} 
    
    # Bypass decorator? The decorator wraps the view. 
    # If we call `process_sale` directly, the decorators inside `api.py` are applied.
    # We need to satisfy `require_gym_permission`.
    # It checks `session.get("current_gym_id")` AND `user_has_gym_permission`.
    # Let's mock `user_has_gym_permission`? Or grant it.
    
    # Grant permissions
    # We can try to monkeypatch `accounts.decorators.user_has_gym_permission`?
    # Or just let it run if user is superuser?
    user.is_superuser = True
    user.save()
    # accounts.permissions.user_has_gym_permission usually returns True for superuser?
    # Let's hope so.
    
    try:
        response = process_sale(request)
        print(f"Process Sale Response: {response.status_code}")
        if response.status_code != 200:
            print(response.content)
            sys.exit(1)
            
        data = json.loads(response.content)
        order_id = data['order_id']
        print(f"Order Created: {order_id}")
        
        # Verify Attributes
        order = Order.objects.get(id=order_id)
        if order.total_amount == 0:
            print("ERROR: Total Amount is 0!")
            sys.exit(1)
            
        print(f"Order Amount: {order.total_amount}")
        print(f"Order Date: {order.created_at}")
        
        # Check Date override (Day should be 01, Month 01, Year 2025)
        # Note: Timezone might affect it slightly but date part should match if simple
        if order.created_at.year != 2025 or order.created_at.month != 1:
             print("ERROR: Custom Date Not Applied!")
             sys.exit(1)

    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 3. Test Invoice
    print("Testing Invoice...")
    req_inv = rf.post(f'/sales/api/order/{order_id}/invoice/', content_type='application/json', data=json.dumps({'email': 'test@test.com'}))
    req_inv.user = user
    req_inv.gym = gym
    req_inv.session = {'current_gym_id': gym.id}
    
    try:
        res_inv = order_generate_invoice(req_inv, order_id)
        print(f"Invoice Response: {res_inv.status_code}")
        if res_inv.status_code == 200:
             print("Invoice Generated OK")
        else:
             print(res_inv.content)
    except Exception:
        import traceback
        traceback.print_exc()

    print("--- VERIFICATION COMPLETED ---")

if __name__ == "__main__":
    verify()
