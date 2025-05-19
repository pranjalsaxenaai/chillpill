from rest_framework.views import APIView
from rest_framework.response import Response
from .services import check_task_status, start_generate_script

class OperationView(APIView):
    def get(self, request):
        operation_id = request.query_params.get('operation_id')
        status = check_task_status(operation_id)
        return Response(
            {"operation_id": operation_id, "status": status},
            status=200)
    
    def post(self, request):
        operation_name = request.data.get('operation_name')
        project_id = request.data.get('project_id')
        project_idea = request.data.get('project_idea')
        print(f"Received request for operation {operation_name} for project {project_id}")
        # Check the operation name and call the appropriate operation
        match operation_name:
            case "generate_script":
                operation_id = start_generate_script(project_id, project_idea)

            case _:
                return Response(
                    {"message": "Unknown operation"},
                    status=400)
        
        return Response(
            {"operation_id": operation_id},
            status=202)
    