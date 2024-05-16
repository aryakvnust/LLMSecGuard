from rest_framework.permissions import BasePermission

class IsPublicOrIsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.public

class IsParentPublicOrIsParentOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.model.user == request.user or obj.model.public
