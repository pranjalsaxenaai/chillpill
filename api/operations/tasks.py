from celery import shared_task
from celery import chain, chord, group
from scripts.services import generate_script
from scenes.services import generate_scenes
from shots.services import generate_shots
from images.services import generate_images

def chain_script_tasks(project_id, project_idea):
    """
    This function orchestrates the entire process of generating a script, scenes, shots, and images.
    
    Args:
        project_id (int): The unique identifier of the project.
        project_idea (str): The idea for the project.

    Returns:
        str: The generated script.
    """
    # Step 1: Generate script
    script_task = generate_script_task.s(project_id, project_idea)

    # Step 2: Generate scenes from script
    scenes_task = generate_scenes_task.s()

    # Step 3: Generate shots from scenes
    shots_group = fanout_and_wait.s()
   

    workflow = chain(
        script_task,
        scenes_task,
        shots_group)

    result = workflow.apply_async()
    return result.id

@shared_task
def fanout_and_wait(scene_ids):
    # Launch group and wait for all to finish, then return results
    result = group(generate_shots_task.s(scene_id) for scene_id in scene_ids)()
    return result.get() # This will block until all tasks in the group are done
# Need to modify and use chord instead of group to get the results. 
# The callback of the chord should set the status of the parent task to success.
# This status should be maintained in a redis database.


@shared_task
def generate_script_task(project_id, project_idea):
    """
    Generates a script based on the provided project ID and project idea.
    Returns the generated script ID.
    """
    script_id = generate_script(project_id, project_idea)
    print(f"Generated script ID: {script_id}")
    return script_id

@shared_task
def generate_scenes_task(script_id):
    """
    Generates scenes for a given script and creates them in the system.

    Args:
        script_id (int): The unique identifier of the script for which scenes are to be generated.

    Returns:
        list: A list of IDs of the created scenes.

    """

    scene_ids = generate_scenes(script_id)
    print(f"Generated scenes IDs: {scene_ids}")
    return scene_ids

@shared_task
def generate_shots_task(scene_id:str):
    """
    Generates shots for a given scene and creates them in the system.

    Args:
        scene_id (int): The unique identifier of the scene for which shots are to be generated.

    Returns:
        list: A list of IDs of the created shots.
    """
    shot_ids = generate_shots(scene_id)
    for shot_id in shot_ids:
        image_ids = generate_images(shot_id)
        if len(image_ids) > 0:
            print(f"Generated imageid {image_ids[0]} for shot ID: {shot_id}")
    print(f"Generated shots IDs: {shot_ids}, for scene ID: {scene_id}")
    return shot_ids

# @shared_task
# def generate_image_task(shot_id):
#     """
#     Generates an image based on the provided shot ID, uploads it to blob storage, 
#     and returns the ID of the created image.

#     Args:
#         shot_id (int): The unique identifier of the shot for which the image is to be generated.

#     Returns:
#         int: The unique identifier of the created image.

#     Note:
#         This function retrieves the shot details using the provided shot ID, generates an image 
#         based on the shot's image prompt, uploads the image to blob storage, and creates a 
#         corresponding image record in the system.
#     """
#     shot = get_shot(shot_id)
#     image_url = generate_image(shot["image_prompt"])
#     # Write Code to copy the image to our blob storage
#     image_id = create_image(image_url)
#     return image_id


