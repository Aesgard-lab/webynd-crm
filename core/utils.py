from .models import SystemLog


def log_action(user, module, action, data=None):
    SystemLog.objects.create(
        user=user,
        module=module,
        action=action,
        data=data or {}
    )
