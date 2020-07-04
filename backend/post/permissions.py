from rest_framework import permissions


class IsAuthorOrReadyOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """Allow owner to edit object, Otherwise read only"""
        
        if request.method in permissions.SAFE_METHODS:
            return True

        # only allow owner to edit their own posts
        return obj.owner and obj.owner == request.user



class IsOwnerAllowedToEditImage(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Allow owner to edit images if it has not beed assigned to a post.
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.post is not None:
            return False
        return True
