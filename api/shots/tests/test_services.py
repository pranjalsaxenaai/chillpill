from django.test import TestCase
from shots.models import Shot
from shots.services import get_shot, create_shot, delete_shot, list_shots
import datetime

class ShotServiceTest(TestCase):
    def setUp(self):
        self.shot = Shot.objects.create(
            scene_id="scene123",
            image_prompt="An Image of a ...",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

    def test_get_shot(self):
        shot = get_shot(self.shot.id)
        self.assertIsNotNone(shot)
        self.assertEqual(shot['scene_id'], "scene123")
        self.assertEqual(shot['image_prompt'], "An Image of a ...")

    def test_list_shots(self):
        Shot.objects.create(
            scene_id="scene789",
            image_prompt="An Image of a Tree",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now())
        
        Shot.objects.create(
            scene_id="scene789",
            image_prompt="An Image of a Car",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

        Shot.objects.create(
            scene_id="scene789",
            image_prompt="An Image of a House",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

        shots = list_shots("scene789")
        self.assertEqual(len(shots), 3)
        self.assertEqual(shots[0]['image_prompt'], "An Image of a Tree")
        self.assertEqual(shots[1]['image_prompt'], "An Image of a Car")
        self.assertEqual(shots[2]['image_prompt'], "An Image of a House")

    def test_create_shot(self):
        shot_id = create_shot(
            "scene456",
            "Image of a Dosa")
        
        self.assertIsNotNone(shot_id)
        shot = Shot.objects.get(id=shot_id)
        self.assertEqual(shot.scene_id, "scene456")
        self.assertEqual(shot.image_prompt, "Image of a Dosa")