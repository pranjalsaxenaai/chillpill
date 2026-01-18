from celery.result import AsyncResult
from api.clients import get_langgraph_client
from projects.services import get_project
from .tasks import chain_script_tasks


def start_generate_script(project_id, project_idea):
    
    # If no project idea is provided, fetch the project idea from the project description
    if project_idea is None:
        # Fetch the project
        project = get_project(project_id)
        project_idea = project["project_desc"]

    # Call the Celery task
    langgraph_client = get_langgraph_client()
    run = langgraph_client.create_run(
        graph_name="kahaaniai",
        input_data={
            "input_idea": project_idea,
            "db_metadata": {"project_id": project_id},
        }
    )
    return run['run_id']

def check_task_status(run_id):
    # Check the task status
    langgraph_client = get_langgraph_client()
    run = langgraph_client.get_run(
        run_id=run_id
    )

    # todo - We don't want to poll for assets generation status from UI
    # todo - Design a flow, where langgraph signals the API to update status in a operations db, and UI polls API for status in DB
    # todo - Design a flow, where API sends the notification somehow to the UI using some websocket or something else.
    return run['status']