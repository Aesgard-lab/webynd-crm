from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from gyms.models import GymMembership

User = get_user_model()

class CanViewKPI(BasePermission):
    """
    - superadmin: acceso total
    - admin/staff: debe tener membresía activa en el gym indicado
      y, si la vista lo requiere, el permiso específico en esa membresía.
    La vista puede declarar `required_perm = "can_manage_cash"` (por ejemplo).
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # superadmin ve todo
        if getattr(user, "effective_role", None) == "superadmin":
            return True

        # gym por query (?gym=ID) o por current_gym del usuario
        gym_id = request.query_params.get("gym") or getattr(user, "current_gym_id", None)
        if not gym_id:
            return False

        membership = GymMembership.objects.filter(
            user=user, gym_id=gym_id, is_active=True
        ).first()
        if not membership:
            return False

        required = getattr(view, "required_perm", None)
        if not required:
            return True

        return bool(getattr(membership, required, False))
