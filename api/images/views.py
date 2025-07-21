from rest_framework.views import APIView
from rest_framework.response import Response
from . import services

class ImageView(APIView):
    def get(self, request):
        shot_id = request.query_params.get('shot_id')
        image_id = request.query_params.get('image_id')
        if(image_id and shot_id):
            return Response({"message": "Both shot_id and image_id cannot be provided"}, status=400)
        
        if(not image_id and not shot_id):
            return Response({"message": "Either shot_id or image_id is required"}, status=400)

        if(image_id):
            scene = services.get_image(image_id)
            if(scene is None):
                return Response({"message": "Image not found"}, status=404)
            return Response(scene)
        
        if(shot_id):
            scenes = services.list_images(shot_id)
            return Response(scenes)