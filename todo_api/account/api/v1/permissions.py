from rest_framework import permissions

class AnonPermissionOnly(permissions.BasePermission):
    """ only unathenticated users can login. """
    def has_permission(self, request, view):
        return not request.user.is_authenticated



class IsAccountOwnerOrReadOnly(permissions.BasePermission):
    message     = "Only account owner can perform this action."
    # Fix IT -> only account owners can delete,update,edit
    def has_object_permission(self,request,view,obj):
        if request.method  in permissions.SAFE_METHODS:
            return True
        return obj.owner.id  == request.user.id

