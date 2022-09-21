from rest_framework.permissions import BasePermission, SAFE_METHODS

SAFE_GET_METHODS = ('GET', 'HEAD', 'OPTIONS')

perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class IsAdminUserOrReadOnly(BasePermission):
    """
    The request is authenticated as an admin user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


class ComplexGuidePermission(BasePermission):

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
                request.user and
                request.user.is_staff):
            return True
        elif (request.method in ('POST', 'PUT', 'PATCH') and
                request.user and request.user.is_authenticated):
            return True
        return False
