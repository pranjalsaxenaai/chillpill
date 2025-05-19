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