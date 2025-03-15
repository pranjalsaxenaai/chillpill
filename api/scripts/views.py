from rest_framework.views import APIView
from rest_framework.response import Response
from . import services

class ScriptView(APIView):
    def get(self, request):
        script_id = request.query_params.get('script_id')
        if(not script_id):
            return Response({"message": "script_id is required"}, status=400)

        script = services.get_script(script_id)
        if(script is None):
            return Response({"message": "Script not found"}, status=404)
        return Response(script)