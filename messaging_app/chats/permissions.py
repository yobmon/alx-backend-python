from rest_framework.permissions import BasePermission, SAFE_METHODS,permmisons
from rest_framework import permissions

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request,
        return obj.user == request.user 

class IsConversationMember(BasePermission):
    """
    Only users involved in the conversation may access or post messages.
    """

    def has_object_permission(self, request, view, obj):
        # conversation.members is assumed to be a ManyToMany field
        return request.user in obj.participants.all()
class IsMessageOwnerOrReadOnly(BasePermission):
    """
    Only the owner of a message can EDIT or DELETE it.
    Other participants can only READ.
    """

    def has_object_permission(self, request, view, obj):
        
        # SAFE methods = GET, HEAD, OPTIONS
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        
        # Only owner can update or delete
        return obj.sender == request.user