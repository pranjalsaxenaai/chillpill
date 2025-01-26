from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from projects.models import Project
import datetime

class ProjectViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.project = Project.objects.create(
            user_id="user123",
            project_title="Test Project",
            project_desc="Test Description",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

    def test_get_project(self):
        response = self.client.get(f'/api/projects?project_id={self.project.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['project_title'], "Test Project")

    def test_create_project(self):
        data = {
            "user_id": "user456",
            "project_title": "New Project",
            "project_desc": "New Description"
        }
        response = self.client.post('/api/projects', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['project_id'])