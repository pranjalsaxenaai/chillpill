from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import services

# Create your views here.

@api_view(['GET'])
def get_user(request):
    user = services.get_user()
    return Response(user, safe=False)