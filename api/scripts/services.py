import datetime
import json
from scripts.models import Script
from scripts.aiservices import generate_script_ai
from projects.services import update_project, get_project

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

def generate_script(project_id, project_idea):
    runOutput = generate_script_ai(project_idea)
    
    # Save the generated script
    script_id = create_script(runOutput["Script"])

    # Update the project with the generated script ID
    project = get_project(project_id)
    result = update_project(
        project_id,
        project["project_title"],
        project["project_desc"], 
        script_id)
    
    if result is None:
        raise Exception("Script Generated but Project Update failed")
    
    if(result):
        print("Project Updated Successfully")
    else:
        raise Exception("Project Not Found")
    
    return script_id