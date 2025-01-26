from django.test import TestCase
from scripts.models import Script
from scripts.services import get_script, create_script, update_script, delete_script
import datetime

class ScriptServiceTest(TestCase):
    def setUp(self):
        self.script = Script.objects.create(
            content="Once upon a time...",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

    def test_get_script(self):
        script = get_script(self.script.id)
        self.assertIsNotNone(script)
        self.assertEqual(script['content'], "Once upon a time...")

    def test_create_script(self):
        script_id = create_script("New script content")
        self.assertIsNotNone(script_id)
        script = Script.objects.get(id=script_id)
        self.assertEqual(script.content, "New script content")