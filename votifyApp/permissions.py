from rest_framework import permissions

class isOwnerOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated 
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if request.user:
            return obj.user == request.user
        else :
            return False

class isVoteAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated 
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if request.user:
            return obj.creator.is_vote_admin
        else :
            return False
        
class isSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated 
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if request.user:
            return (obj.creator.is_admin
                    and obj.creator.is_staff
                    and obj.creator.is_superuser )
        else :
            return False
    

