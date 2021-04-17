from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsUserActive(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_active
