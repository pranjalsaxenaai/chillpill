from django.test import TestCase
from images.models import Image
from images.services import get_image, create_image, delete_image, list_images
import datetime

class ImageServiceTest(TestCase):
    def setUp(self):
        self.image = Image.objects.create(
            image_prompt_id="imagePrompt123",
            blob_url="http://www.aiimage.com",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

    def test_get_image(self):
        image = get_image(self.image.id)
        self.assertIsNotNone(image)
        self.assertEqual(image['image_prompt_id'], "imagePrompt123")
        self.assertEqual(image['blob_url'], "http://www.aiimage.com")

    def test_list_images(self):
        Image.objects.create(
            image_prompt_id="imagePrompt789",
            blob_url="http://www.aiimage.com/1",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now())
            
        Image.objects.create(
            image_prompt_id="imagePrompt789",
            blob_url="http://www.aiimage.com/2",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        Image.objects.create(
            image_prompt_id="imagePrompt789",
            blob_url="http://www.aiimage.com/3",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

        images = list_images("imagePrompt789")
        self.assertEqual(len(images), 3)
        self.assertEqual(images[0]['blob_url'], "http://www.aiimage.com/1")
        self.assertEqual(images[1]['blob_url'], "http://www.aiimage.com/2")
        self.assertEqual(images[2]['blob_url'], "http://www.aiimage.com/3")

    def test_create_image(self):
        image_id = create_image(
            "imagePrompt456",
            "http://www.aiimage.com/newimage")
        
        self.assertIsNotNone(image_id)
        image = Image.objects.get(id=image_id)
        self.assertEqual(image.image_prompt_id, "imagePrompt456")
        self.assertEqual(image.blob_url, "http://www.aiimage.com/newimage")