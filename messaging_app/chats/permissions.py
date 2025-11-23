from rest_framework.permissions import BasePermission, SAFE_METHODS


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