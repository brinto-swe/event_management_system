from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def in_groups_required(*group_names):
    def check(user):
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if user.groups.filter(name__in=group_names).exists():
            return True
        return False
    return user_passes_test(check)

def require_admin(user):
    if user.is_superuser or user.groups.filter(name='Admin').exists():
        return True
    raise PermissionDenied
