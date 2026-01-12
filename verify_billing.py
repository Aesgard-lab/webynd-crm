import os
import sys
import django
from django.test import RequestFactory
from django.template.loader import render_to_string

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from finance.views import billing_dashboard
from organizations.models import Gym
from django.contrib.auth import get_user_model
from finance.models import PaymentMethod

def verify():
    print("--- VERIFYING BILLING DASHBOARD RENDER ---")
    try:
        User = get_user_model()
        gym, _ = Gym.objects.get_or_create(name="Verify Gym")
        user = User.objects.filter(gym_memberships__gym=gym).first()
        if not user:
             user = User.objects.create_user("billing_verifier", "pass")
             from django.apps import apps
             GymMembership = apps.get_model('accounts', 'GymMembership')
             GymMembership.objects.create(user=user, gym=gym, role='ADMIN')
             user.is_superuser = True
             user.save()

        # Ensure active payment method for filters
        PaymentMethod.objects.get_or_create(gym=gym, name="Test Method", is_active=True)

        req = RequestFactory().get('/finance/report/billing/')
        req.user = user
        req.gym = gym 
        req.session = {'current_gym_id': gym.id} # Mock session with ID
        
        # Test View execution (returns HttpResponse)
        response = billing_dashboard(req)
        print(f"View Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Render Success!")
            # Basic content check
            content = response.content.decode('utf-8')
            if "Informe de Ventas" in content and "canvas id=\"revenueChart\"" in content:
                print("Content Checks Passed (Title + Chart found)")
            else:
                print("WARNING: Key elements missing in content")
        else:
             print("View returned error status")
             sys.exit(1)

    except Exception as e:
        print("\n!!! ERROR !!!")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    verify()
