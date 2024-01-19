from rest_framework.permissions import BasePermission

from snack.core.constants import MemberType


class IsAdmin(BasePermission):
    """
    Allows access only member_type is admin
    """

    def has_permission(self, request, view):
        if request.user.member_type == MemberType.ADMIN:
            return True
        else:
            return False


class IsActive(BasePermission):
    """
    Allows access only NOT DELETED And ACTIVE User
    """

    def has_permission(self, request, view):
        if request.user.is_deleted:
            return False
        if not request.user.is_active:
            return False
        return True
