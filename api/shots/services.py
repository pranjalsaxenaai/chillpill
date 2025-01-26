import datetime
import json
from shots.models import Shot

def get_shot(shot_id):
    sceneShot = Shot.objects(id=shot_id, is_deleted__ne=True).first()
    return json.loads(sceneShot.to_json()) if sceneShot else None

# List all shots of a scene
def list_shots(scene_id):
    sceneShots = (
        Shot.objects(scene_id=scene_id, is_deleted__ne=True)
    )
    return json.loads(sceneShots.to_json())

# Create a new scene
def create_shot(scene_id, image_prompt):
    shot = Shot(
            scene_id=scene_id,
            image_prompt=image_prompt,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now())
   
    try:
        shot.save()
    except Exception as e:
        print(e)
        return None   
    return str(shot.id)

def update_script(shot_id, scene_id, image_prompt):
    shot = Shot.objects(id=shot_id).first()
    if shot and shot.is_deleted == False:
        shot.scene_id = scene_id
        shot.image_prompt = image_prompt
        shot.updated_at = datetime.datetime.now()
        try:
            shot.save()
            return True
        except Exception as e:
            print(e)
            return None
    return False

def delete_shot(shot_id):
    shot = Shot.objects(id=shot_id).first()
    if shot and shot.is_deleted == False:
        shot.modified_at = datetime.datetime.now()
        shot.is_deleted = True
        shot.save()
        return True
    return False