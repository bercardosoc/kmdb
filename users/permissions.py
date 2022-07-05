from rest_framework.permissions import BasePermission
from rest_framework.views import Request 

class UserPermission(BasePermission):

    def has_permission(self, request: Request, _):

        staff_methods = {
            "GET",
        }

        if request.method in staff_methods:
            return request.user.is_staff 

        return True 