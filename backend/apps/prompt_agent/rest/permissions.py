from rest_framework.permissions import BasePermission

class IsPublicOrIsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.is_public

class IsParentPublicOrIsParentOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.model.user == request.user or obj.model.is_public
