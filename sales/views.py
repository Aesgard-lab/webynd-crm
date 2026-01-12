from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import require_gym_permission

from finance.models import PaymentMethod

@login_required
@require_gym_permission('sales.view_sale') # Assuming a permission exists or we use a basic one
def pos_home(request):
    gym = request.gym
    payment_methods = PaymentMethod.objects.filter(gym=gym, is_active=True)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # Get staff (anyone with membership in this gym)
    # Ideally filter by role, but strict staff check is fine
    staff_users = User.objects.filter(gym_memberships__gym=gym, gym_memberships__is_active=True).distinct()
    
    return render(request, 'backoffice/sales/pos.html', {
        'title': 'TPV / POS',
        'payment_methods': payment_methods,
        'staff_users': staff_users
    })
