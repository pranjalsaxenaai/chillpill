import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from projects.models import Project

def get_project(project_id):
    return None
def get_projects(user_id):
    return None

def create_project(user_id, project_title, project_desc):
    uri = "mongodb+srv://pranjalsaxenaai:0Z7y7Y9liViFQBBQ@chillpilldb.qzc1d.mongodb.net/?retryWrites=true&w=majority&appName=chillpilldb"

    with MongoClient(uri, server_api=ServerApi('1')) as client:
        try:
            db = client.chillpilldb

            # Creating a collection in MongoDB
            db_projects = db["projects"]

            # Inserting a Project Model Object in MongoDB
            project = Project(
                    user_id=user_id,
                    project_title=project_title,
                    project_desc=project_desc,
                    created_at=datetime.now())
            
            result = db_projects.insert_one(project.to_mongo())
            project.id = result.inserted_id

        except Exception as e:
            print(e)
            return None    
    return project