from django.test import TestCase
from projects.models import Project
import datetime

class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            user_id="user123",
            project_title="Test Project",
            project_desc="Test Description",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

    def test_project_creation(self):
        self.assertEqual(self.project.project_title, "Test Project")
        self.assertEqual(self.project.project_desc, "Test Description")
        self.assertEqual(self.project.user_id, "user123")
        self.assertFalse(self.project.is_deleted)