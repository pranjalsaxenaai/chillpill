import datetime
import json
from projects.models import Project

def get_project(project_id):
    userProject = Project.objects(id=project_id, is_deleted__ne=True).first()
    return json.loads(userProject.to_json()) if userProject else None

def list_projects(user_id):
    userProjects = (
        Project.objects(user_id=user_id, is_deleted__ne=True)
        .only('id', 'project_title', 'project_desc', 'updated_at')
    )
    return json.loads(userProjects.to_json())

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

def delete_project(project_id):
    project = Project.objects(id=project_id).first()
    if project and project.is_deleted == False:
        project.modified_at = datetime.datetime.now()
        project.is_deleted = True
        project.save()
        return True
    return False

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