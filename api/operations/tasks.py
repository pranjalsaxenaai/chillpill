from celery import shared_task
from scripts.aiservices import generate_script
from scenes.aiservices import generate_scenes
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
    else:
        raise Exception("Project Not Found")

    # Create Scenes from the generated script
    scenes = generate_scenes(runOutput["Script"])

    for scene in scenes:
        # Save the scene
        create_scene(scene)

    print("Scenes Created Successfully")

    # Create Shots from the generated scenes
    # shots = generate_shots(scenes)

