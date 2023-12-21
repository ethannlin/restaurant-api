from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists() or request.user.is_superuser
    
class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='delivery crew').exists() or request.user.is_superuser
    
class IsManagerOrDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists() or request.user.groups.filter(name='delivery crew').exists() or request.user.is_superuser
    
class IsManagerOrCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists() or not request.user.groups.filter(name='delivery crew').exists() or request.user.is_superuser
    
class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name='manager').exists() and not request.user.groups.filter(name='delivery_crew').exists() or request.user.is_superuser 