import os
import sys
import django
from django.template.loader import render_to_string
from django.test import RequestFactory

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from organizations.models import Gym
from clients.models import Client
from sales.models import Order
from django.contrib.auth import get_user_model

def verify_render():
    print("--- VERIFYING DETAIL RENDER ---")
    try:
        # 1. Setup Data
        User = get_user_model()
        gym, _ = Gym.objects.get_or_create(name="Verify Gym")
        user = User.objects.filter(gym_memberships__gym=gym).first()
        if not user:
             user = User.objects.create_user("dummy_detail", "pass")
        
        client = Client.objects.create(gym=gym, first_name="Detail", last_name="Client")
        
        # Create Order
        Order.objects.create(gym=gym, client=client, created_by=user, total_amount=10)

        # 2. Context
        req = RequestFactory().get('/fake')
        req.user = user
        from django.contrib.sessions.middleware import SessionMiddleware
        req.session = {}
        
        context = {
            'client': client,
            'visits': [],
            'invoices': [], # Assuming view passes these
            'request': req,
        }
        
        # 3. Render
        print("Rendering 'backoffice/clients/detail.html'...")
        rendered = render_to_string('backoffice/clients/detail.html', context)
        print("Render Success! Length:", len(rendered))
        
    except Exception as e:
        print("\n!!! RENDER ERROR !!!")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    verify_render()
