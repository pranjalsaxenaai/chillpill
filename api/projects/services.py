import datetime
import json
from projects.models import Project

# Get a project by its ID
def get_project(project_id):
    userProject = Project.objects(id=project_id, is_deleted__ne=True).first()
    return json.loads(userProject.to_json()) if userProject else None

# List all projects of a user
def list_projects(user_id):
    userProjects = (
        Project.objects(user_id=user_id, is_deleted__ne=True)
    )
    return json.loads(userProjects.to_json())

# Create a new project
def create_project(user_id, project_title, project_desc):
    project = Project(
            user_id=user_id,
            project_title=project_title,
            project_desc=project_desc,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now())
    
    try:
        project.save()
    except Exception as e:
        print(e)
        return None   
    return str(project.id)

# Delete a project
def delete_project(project_id):
    project = Project.objects(id=project_id).first()
    if project and project.is_deleted == False:
        project.modified_at = datetime.datetime.now()
        project.is_deleted = True
        project.save()
        return True
    return False

# Update a project
def update_project(project_id, project_title, project_desc, script_id):
    project = Project.objects(id=project_id).first()
    if project and project.is_deleted == False:
        project.project_title = project_title
        project.project_desc = project_desc
        project.script_id = script_id
        project.updated_at = datetime.datetime.now()
        try:
            project.save()
            return True
        except Exception as e:
            print(e)
            return None
    return False