from rest_framework.permissions import BasePermission

from users.models import UserProfile


class IsBusinessAccount(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.type == UserProfile.TYPE_BUSINESS
