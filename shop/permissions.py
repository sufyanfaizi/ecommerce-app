from rest_framework.permissions import BasePermission
from shop.enums import PermissionGroup

class ProductPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=PermissionGroup.PRODUCT_MANAGER.value).exists()
