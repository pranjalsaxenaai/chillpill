from .tasks import ladder_all_task
from celery.result import AsyncResult
from projects.services import get_project


def start_generate_script(project_id, project_idea):
    
    # If no project idea is provided, fetch the project idea from the project description
    if project_idea is None:
        # Fetch the project
        project = get_project(project_id)
        project_idea = project["project_desc"]

    # Call the Celery task
    task = ladder_all_task.delay(project_id, project_idea)
    return task.id

def check_task_status(task_id):
    # Check the task status
    task = AsyncResult(task_id)
    return task.status