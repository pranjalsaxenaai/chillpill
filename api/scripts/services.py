import datetime
import json
from scripts.models import Script

def get_script(script_id):
    projectScript = Script.objects(id=script_id, is_deleted__ne=True).first()
    return json.loads(projectScript.to_json()) if projectScript else None

# Create a new script
def create_script(content):
    script = Script(
            content=content,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now())
   
    try:
        script.save()
    except Exception as e:
        print(e)
        return None   
    return str(script.id)

def update_script(script_id, content):
    script = Script.objects(id=script_id).first()
    if script and script.is_deleted == False:
        script.content = content
        script.updated_at = datetime.datetime.now()
        try:
            script.save()
            return True
        except Exception as e:
            print(e)
            return None
    return False

def delete_script(script_id):
    script = Script.objects(id=script_id).first()
    if script and script.is_deleted == False:
        script.modified_at = datetime.datetime.now()
        script.is_deleted = True
        script.save()
        return True
    return False