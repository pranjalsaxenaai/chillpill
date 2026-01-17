from .api_client import APIClient
from auth.token_issuer import TokenIssuer
import os

class DBAPIClient:
    def __init__(self, token_issuer):
        self.client = APIClient(base_url=os.getenv("API_BASE_URL"))
        self.token_issuer = token_issuer

    def create_script(self, project_id, script_data):
        token_issuer
        response = self.client.post(
            "/api/scripts",
            data={"script": script_data, "project_id": project_id},
            token=self.token_issuer.get_id_token()
        )
        return response

    def get_script(self, script_id):
        response = self.client.get(f"/api/scripts/{script_id}/", token=self.token_issuer.get_id_token())
        return response.json()

    def update_project(self, project_id, title, description, script_id):
        response = self.client.put(
            f"/api/projects/{project_id}/",
            data={
                "project_title": title,
                "project_desc": description,
                "script_id": script_id
            },
            token=self.token_issuer.get_id_token()
        )
        return response.json()

token_issuer = TokenIssuer()
db_api_client = DBAPIClient(token_issuer=token_issuer)