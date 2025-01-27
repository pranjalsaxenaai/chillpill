def generate_script(project_id):
    # Add wait time to simulate a long running task
    import time
    print(f"Generating script for project {project_id}")
    time.sleep(10)
    print(f"Generated script for project {project_id}")