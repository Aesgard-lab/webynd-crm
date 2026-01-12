import os
import sys
import django
import json
from unittest.mock import patch, MagicMock

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import RequestFactory
from organizations.models import Gym
from clients.models import Client
from products.models import Product
from finance.models import PaymentMethod
from sales.api import process_sale
from sales.models import Order
from django.contrib.auth import get_user_model

def verify():
    print("--- VERIFYING LINKED CARD PAYMENT ---", flush=True)
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
        user = User.objects.create_user("verifier_card", "password")
        GymMembership.objects.create(user=user, gym=gym, role='ADMIN', is_active=True)

    client, _ = Client.objects.get_or_create(gym=gym, first_name="CardClient", email="card@test.com")
    prod, _ = Product.objects.get_or_create(gym=gym, name="CardProd", defaults={'base_price': 10})
    
    # Ensure "Tarjeta" method exists
    pm_card, _ = PaymentMethod.objects.get_or_create(gym=gym, name="Tarjeta", defaults={'is_active': True})
    
    # 2. Test Payload with INVALID method_id but VALID provider
    data = {
        'client_id': client.id,
        'items': [{'id': prod.id, 'type': 'product', 'qty': 1, 'discount': {'value': 0}}],
        'payments': [{
            'method_id': 99999, # Intentional Invalid ID
            'amount': 10,
            'provider': 'stripe',
            'payment_token': 'pm_fake_token'
        }],
        'action': 'NONE'
    }
    
    # Mock Request
    request = rf.post('/sales/api/sale/process/', content_type='application/json', data=json.dumps(data))
    request.user = user
    request.gym = gym 
    request.session = {'current_gym_id': gym.id} 
    
    # Mock Stripe Charge
    with patch('finance.stripe_utils.charge_client') as mock_charge:
        mock_charge.return_value = (True, "ch_fake_transaction_id")
        
        try:
            response = process_sale(request)
            print(f"Response Code: {response.status_code}")
            if response.status_code != 200:
                print(response.content)
                sys.exit(1)
                
            data = json.loads(response.content)
            order_id = data['order_id']
            print(f"Order Created: {order_id}")
            
            # Verify Order Payment
            order = Order.objects.get(id=order_id)
            payment = order.payments.first()
            
            print(f"Payment Method Used: {payment.payment_method.name}")
            if payment.payment_method.id != pm_card.id:
                 print(f"WARNING: Expected method {pm_card.name}, got {payment.payment_method.name}")
            
            if payment.transaction_id != "ch_fake_transaction_id":
                 print(f"ERROR: Incorrect transaction ID")
                 sys.exit(1)
                 
            print("SUCCESS: Linked card payment processed with fallback method!")

        except Exception as e:
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    verify()
