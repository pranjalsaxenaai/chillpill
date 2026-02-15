from rest_framework.views import APIView
from rest_framework.response import Response
from . import services

class ShotView(APIView):
    def get(self, request):
        scene_id = request.query_params.get('scene_id')
        shot_id = request.query_params.get('shot_id')
        if(scene_id and shot_id):
            return Response({"message": "Both scene_id and shot_id cannot be provided"}, status=400)
        
        if(not scene_id and not shot_id):
            return Response({"message": "Either scene_id or shot_id is required"}, status=400)

        if(shot_id):
            shot = services.get_shot(shot_id)
            if(shot is None):
                return Response({"message": "Shot not found"}, status=404)
            return Response(shot)
        
        if(scene_id):
            shots = services.list_shots(scene_id)
            return Response(shots)

    def post(self, request):
        scene_id = request.data.get('scene_id')
        shot_data = request.data.get('shot')
        if not scene_id or not shot_data:
            return Response({"message": "scene_id and shot data are required"}, status=400)

        shot = services.create_shot(scene_id, shot_data)
        if shot is None:
            return Response({"message": "Failed to create shot"}, status=500)

        return Response(shot, status=201)