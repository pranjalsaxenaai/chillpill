from rest_framework.views import APIView
from rest_framework.response import Response
from . import services
from api.utils.permissions import IsOwner

class ScriptView(APIView):
    permission_classes = [IsOwner]
    def get(self, request):
        print("ScriptView GET request received")
        print("User Email ID:", request.user.email)  # This will print the user email if authenticated
        script_id = request.query_params.get('script_id')
        if(not script_id):
            return Response({"message": "script_id is required"}, status=400)

        script = services.get_script(script_id)
        self.check_object_permissions(request, script)
        if(script is None):
            return Response({"message": "Script not found"}, status=404)
        return Response(script)