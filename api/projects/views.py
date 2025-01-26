from rest_framework.views import APIView
from rest_framework.response import Response
from . import services

class ProjectView(APIView):
    def get(self, request):
        project_id = request.query_params.get('project_id')
        user_id = request.query_params.get('user_id')
        if(project_id and user_id):
            return Response({"message": "Both project_id and user_id cannot be provided"}, status=400)
        
        if(not project_id and not user_id):
            return Response({"message": "Either project_id or user_id is required"}, status=400)

        if(project_id):
            project = services.get_project(project_id)
            if(project is None):
                return Response({"message": "Project not found"}, status=404)
            return Response(project)
        
        if(user_id):
            projects = services.list_projects(user_id)
            return Response(projects)

    def post(self, request):
        user_id = request.data.get('user_id')
        project_title = request.data.get('project_title')
        project_desc = request.data.get('project_desc')

        # Validating input parameters
        if not user_id or not project_title or not project_desc:
            return Response({"message": "User ID, Project Title, and Project Description are required"}, status=400)
        
        # Calling service to create project document
        result = services.create_project(user_id, project_title, project_desc)

        # If unknown exception, Returning 500 response
        if(result is None):
            return Response({"message": "Project creation failed"}, status=500)
        
        # Returning 201 response with project_id
        return Response({"message": "Project Created Successfully", "project_id": result}, status=201)
    
    def delete(self, request):
        project_id = request.query_params.get('project_id')
        if not project_id:
            return Response({"message": "project_id is required"}, status=400)
        
        result = services.delete_project(project_id)
        if(result):
            return Response({"message": "Project Deleted Successfully"}, status=200)
        return Response({"message": "Project not found"}, status=404)
    
    def put(self, request):
        project_id = request.data.get('project_id')
        project_title = request.data.get('project_title')
        project_desc = request.data.get('project_desc')
        script_id = request.data.get('script_id')

        # Validating input parameters
        if not project_id:
            return Response({"message": "project_id is required"}, status=400)
        
        if not project_title and not project_desc and not script_id:
            return Response({"message": "Atleast one of project_title, project_desc, script_id is required"}, status=400)
        
        result = services.update_project(project_id, project_title, project_desc, script_id)
        if result is None:
            return Response({"message": "Project Update failed"}, status=500)
        if(result):
            return Response({"message": "Project Updated Successfully"}, status=200)
        return Response({"message": f"Project with id {project_id} not found"}, status=404)