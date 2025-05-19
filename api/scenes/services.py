import datetime
import json
from scenes.models import Scene
from scripts.services import get_script
from scenes.aiservices import generate_scenes_ai
from utils.db_utils import DBUtils

def get_scene(scene_id):
    scriptScene = Scene.objects(id=scene_id, is_deleted__ne=True).first()
    return json.loads(scriptScene.to_json()) if scriptScene else None

def list_scenes(script_id):
    scriptScenes = Scene.objects(script_id=script_id, is_deleted__ne=True)
    scenes_list = [DBUtils.convert_mongo_id(json.loads(scene.to_json())) for scene in scriptScenes]
    return scenes_list

def create_scene(script_id, content):
    scene = Scene(
            content=content,
            script_id=script_id,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now())
    try:
        scene.save()
    except Exception as e:
        print(e)
        return None   
    return str(scene.id)

def update_scene(scene_id, script_id, content):
    scene = Scene.objects(id=scene_id).first()
    if scene and scene.is_deleted == False:
        scene.script_id = script_id
        scene.content = content
        scene.updated_at = datetime.datetime.now()
        try:
            scene.save()
            return True
        except Exception as e:
            print(e)
            return None
    return False

def delete_scene(scene_id):
    scene = Scene.objects(id=scene_id).first()
    if scene and scene.is_deleted == False:
        scene.modified_at = datetime.datetime.now()
        scene.is_deleted = True
        scene.save()
        return True
    return False

def generate_scenes(script_id):
    script = get_script(script_id)
    scenes = generate_scenes_ai(script["content"])
    created_scene_ids = [create_scene(script_id, scene) for scene in scenes]
    return created_scene_ids