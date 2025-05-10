from celery import shared_task
from celery import chain, chord, group
from scripts.services import generate_script
from scenes.services import generate_scenes
from shots.services import generate_shots
#from images.aiservices import generate_image

@shared_task
def fanout_shots(scene_ids):
    """
    This task dynamically creates a group to generate shots parallelly.
    
    Args:
        scenes (list): A list of scenes for which shots are to be generated.

    Returns:
        AsyncResult: The result of the group task.
    """
    return group(generate_shots_task.s(scene_id) for scene_id in scene_ids).apply_async()

@shared_task
def ladder_all_task(project_id, project_idea):
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
    shots_task_group = fanout_shots.s()

    chain(
        script_task,
        scenes_task,
        shots_task_group
    ).apply_async()



@shared_task
def generate_script_task(project_id, project_idea):
    """
    Generates a script based on the provided project ID and project idea.
    Returns the generated script ID.
    """
    return generate_script(project_id, project_idea)

@shared_task
def generate_scenes_task(script_id):
    """
    Generates scenes for a given script and creates them in the system.

    Args:
        script_id (int): The unique identifier of the script for which scenes are to be generated.

    Returns:
        list: A list of IDs of the created scenes.

    """
    return generate_scenes(script_id)

@shared_task
def generate_shots_task(scene_id):
    """
    Generates shots for a given scene and creates them in the system.

    Args:
        scene_id (int): The unique identifier of the scene for which shots are to be generated.

    Returns:
        list: A list of IDs of the created shots.
    """
    return generate_shots(scene_id)

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


