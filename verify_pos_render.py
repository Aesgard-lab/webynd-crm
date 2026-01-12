import os
import sys
import django
from django.conf import settings
from django.template.loader import render_to_string
from django.test import RequestFactory

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from finance.models import PaymentMethod
from organizations.models import Gym
from django.contrib.auth import get_user_model

def verify_render():
    print("--- VERIFYING POS RENDER ---")
    try:
        # 1. Setup Data
        User = get_user_model()
        gym, _ = Gym.objects.get_or_create(name="Verify Gym")
        
        # Ensure we have a user
        user = User.objects.filter(gym_memberships__gym=gym).first()
        if not user:
            print("Creating dummy user for context")
            user = User.objects.create_user("dummy_staff", "pass")
            from django.apps import apps
            GymMembership = apps.get_model('accounts', 'GymMembership')
            GymMembership.objects.create(user=user, gym=gym, role='STAFF')

        # 2. Context Data (mimicking views.py)
        payment_methods = PaymentMethod.objects.filter(gym=gym, is_active=True)
        staff_users = User.objects.filter(gym_memberships__gym=gym, gym_memberships__is_active=True).distinct()
        
        req = RequestFactory().get('/fake')
        req.user = user
        from django.contrib.sessions.middleware import SessionMiddleware
        # Simple mock
        req.session = {}
        context = {
            'title': 'TPV / POS',
            'payment_methods': payment_methods,
            'staff_users': staff_users,
            'request': req, 
            'csrf_token': 'dummy' 
        }
        
        # 3. Render
        print("Rendering 'backoffice/sales/pos.html'...")
        rendered = render_to_string('backoffice/sales/pos.html', context)
        print("Render Success! Length:", len(rendered))
        
    except Exception as e:
        print("\n!!! RENDER ERROR !!!")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    verify_render()
