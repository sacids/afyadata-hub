
from rest_framework import permissions
from .models import AuthorizedInstance

class HasValidInstanceKey(permissions.BasePermission):
    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_X_API_KEY')
        if not api_key:
            return False

        try:
            instance = AuthorizedInstance.objects.get(api_key=api_key, is_active=True)
            request.instance_auth = instance 
            return True
        except AuthorizedInstance.DoesNotExist:
            return False