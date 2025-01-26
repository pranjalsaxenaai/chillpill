from django.test import TestCase
from projects.models import Project
from projects.services import get_project, create_project
import datetime

class ProjectServiceTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            user_id="user123",
            project_title="Test Project",
            project_desc="Test Description",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

    def test_get_project(self):
        project = get_project(self.project.id)
        self.assertIsNotNone(project)
        self.assertEqual(project['project_title'], "Test Project")

    def test_create_project(self):
        project_id = create_project("user456", "New Project", "New Description")
        self.assertIsNotNone(project_id)
        project = Project.objects.get(id=project_id)
        self.assertEqual(project.project_title, "New Project")
        self.assertEqual(project.project_desc, "New Description")