from  rest_framework.permissions import BasePermission

class IsOwner(BasePermission):  # BasePermission is used for creating custom permissions
    def has_object_permission(self, request, view, obj):

        # Each object in our system has a FK relationship to some project document.
        # The project object has a user_email field that indicates the owner of the project.
        # We check if the user making the request is the owner of the project.
        
        return obj.project.user_email == request.user.email