import datetime
import json
from images.models import Image

# Get a image by its ID
def get_image(image_id):
    image = Image.objects(id=image_id, is_deleted__ne=True).first()
    return json.loads(image.to_json()) if image else None

# List all images of an image prompt
def list_images(image_prompt_id):
    imagePromptImages = (
        Image.objects(image_prompt_id=image_prompt_id, is_deleted__ne=True)
    )
    return json.loads(imagePromptImages.to_json())

# Create a new image
def create_image(image_prompt_id, blob_url):
    image = Image(
            image_prompt_id=image_prompt_id,
            blob_url=blob_url,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now())
    
    try:
        image.save()
    except Exception as e:
        print(e)
        return None   
    return str(image.id)

# Delete an image
def delete_image(image_id):
    image = Image.objects(id=image_id).first()
    if image and image.is_deleted == False:
        image.modified_at = datetime.datetime.now()
        image.is_deleted = True
        image.save()
        return True
    return False
