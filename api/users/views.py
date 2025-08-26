from rest_framework.views import APIView
from rest_framework.response import Response
from exceptions.resource_exceptions import ResourceConflictException, UnhandledResourceException
from . import services

# Create your views here.

class UserView(APIView):
    def get(self, request):
        # request.user is populated by the authentication middleware (from the token, not from query params)
        # The token is validated to ensure authenticity
        user = services.get_user(request.user.email)
        if user is None:
            return Response({"message": "User not found"}, status=404)
        return Response(user)
    
    def post(self, request):
        email = request.user.email
        name = request.user.name
        given_name = request.user.given_name
        family_name = request.user.family_name

        if not email or not name:
            return Response({"message": "Email and Name are required"}, status=400)

        try:
            user = services.create_user(email, name, given_name, family_name)
        except ResourceConflictException as e:
            return Response({"message": e.default_detail}, status=e.status_code)
        except UnhandledResourceException as e:
            return Response({"message": e.default_detail}, status=e.status_code)

        return Response({"message": "User Created Successfully", "user_id": user}, status=201)