from rest_framework.views import APIView
from rest_framework.response import Response
from . import services

class SceneView(APIView):
    def get(self, request):
        script_id = request.query_params.get('script_id')
        scene_id = request.query_params.get('scene_id')
        if(script_id and scene_id):
            return Response({"message": "Both script_id and scene_id cannot be provided"}, status=400)
        
        if(not script_id and not scene_id):
            return Response({"message": "Either script_id or scene_id is required"}, status=400)

        if(scene_id):
            scene = services.get_scene(scene_id)
            if(scene is None):
                return Response({"message": "Scene not found"}, status=404)
            return Response(scene)
        
        if(script_id):
            scenes = services.list_scenes(script_id)
            return Response(scenes)
        
    def post(self, request):
        script_id = request.data.get('script_id')
        scene_data = request.data.get('scene')
        if not script_id or not scene_data:
            return Response({"message": "script_id and scene data are required"}, status=400)

        scene = services.create_scene(script_id, scene_data)
        if scene is None:
            return Response({"message": "Failed to create scene"}, status=500)

        return Response(scene, status=201)