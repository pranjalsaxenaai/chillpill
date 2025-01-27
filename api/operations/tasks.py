from celery import shared_task
import time

@shared_task
def generate_script_all(project_id):
    # Add wait time to simulate a long running task
    print(f"Generating script for project {project_id}")
    time.sleep(10)
    print(f"Generated script for project {project_id}")
    