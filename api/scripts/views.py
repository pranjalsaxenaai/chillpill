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

    def post(self, request):
        print("ScriptView POST request received")
        print("User Email ID:", request.user.email)  # This will print the user email if authenticated
        script_data = request.data.get('script')
        project_id = request.data.get('project_id')
        if(not script_data):
            return Response({"message": "script is required"}, status=400)

        if(not project_id):
            return Response({"message": "project_id is required"}, status=400)

        script = services.create_script(script_data)
        if(script is None):
            return Response({"message": "Failed to create script"}, status=500)

        project = services.get_project(project_id)
        if project is None:
            return Response({"message": "Project not found"}, status=404)

        result = services.update_project(
            project_id,
            project["project_title"],
            project["project_desc"],
            script
        )

        if result is None:
            return Response({"message": "Failed to update project"}, status=500)

        return Response(script, status=201)