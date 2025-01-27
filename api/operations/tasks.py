from celery import shared_task
from scripts.aiservices import generate_script
from scripts.services import create_script
from projects.services import update_project

@shared_task
def generate_script_all(project_id, project_idea):
    runOutput, project = generate_script(project_id, project_idea)
    
    # Save the generated script
    script_id = create_script(runOutput["Script"])

    # Update the project with the generated script ID
    result = update_project(
        project_id,
        project["project_title"],
        project["project_desc"], 
        script_id)
    
    if result is None:
        raise Exception("Script Generated but Project Update failed")
    
    if(result):
        print("Project Updated Successfully")
        return
    raise Exception("Project Not Found")

