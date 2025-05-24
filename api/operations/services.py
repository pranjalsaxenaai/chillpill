from celery.result import AsyncResult
from projects.services import get_project
from .tasks import chain_script_tasks


def start_generate_script(project_id, project_idea):
    
    # If no project idea is provided, fetch the project idea from the project description
    if project_idea is None:
        # Fetch the project
        project = get_project(project_id)
        project_idea = project["project_desc"]

    # Call the Celery task
    taskId = chain_script_tasks(project_id, project_idea)
    return taskId

def check_task_status(task_id):
    # Check the task status
    task = AsyncResult(task_id)
    return task.status