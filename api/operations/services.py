from .tasks import generate_script_all
from celery.result import AsyncResult


def start_generate_script(project_id, project_idea):
    # Call the Celery task
    task = generate_script_all.delay(project_id, project_idea)

    return task.id

def check_task_status(task_id):
    # Check the task status
    task = AsyncResult(task_id)
    return task.status