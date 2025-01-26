from django.test import TestCase
from scenes.models import Scene
from scenes.services import get_scene, create_scene, delete_scene, list_scenes
import datetime

class SceneServiceTest(TestCase):
    def setUp(self):
        self.scene = Scene.objects.create(
            script_id="script123",
            content="Scene Content",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

    def test_get_scene(self):
        scene = get_scene(self.scene.id)
        self.assertIsNotNone(scene)
        self.assertEqual(scene['script_id'], "script123")
        self.assertEqual(scene['content'], "Scene Content")

    def test_list_scenes(self):
        Scene.objects.create(
            script_id="script789",
            content="Scene Content 1",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now())
        
        Scene.objects.create(
            script_id="script789",
            content="Scene Content 2",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        Scene.objects.create(
            script_id="script789",
            content="Scene Content 3",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

        scenes = list_scenes("script789")
        self.assertEqual(len(scenes), 3)
        self.assertEqual(scenes[0]['content'], "Scene Content 1")
        self.assertEqual(scenes[1]['content'], "Scene Content 2")
        self.assertEqual(scenes[2]['content'], "Scene Content 3")

    def test_create_scene(self):
        scene_id = create_scene(
            "script456",
            "I once had a dream")
        
        self.assertIsNotNone(scene_id)
        scene = Scene.objects.get(id=scene_id)
        self.assertEqual(scene.script_id, "script456")
        self.assertEqual(scene.content, "I once had a dream")