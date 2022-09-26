from rest_framework.permissions import BasePermission, SAFE_METHODS


class ComplexGuidePermission(BasePermission):
    """
    The request is authenticated as a staff, or is a read-only request,
    or is authenticated and method is not DELETE.
    Deletion is allowed only to staff.
    """

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
                request.user and
                request.user.is_staff):
            return True
        elif (request.method in ('POST', 'PUT', 'PATCH') and
                request.user and request.user.is_authenticated):
            return True
        return False
