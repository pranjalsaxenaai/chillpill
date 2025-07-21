import datetime
import json, base64
from images.models import Image
from shots.services import get_shot
from images.aiservices import generate_image_ai
import os
from io import BytesIO
import boto3


# Get a image by its ID
def get_image(image_id):
    image = Image.objects(id=image_id, is_deleted__ne=True).first()
    return json.loads(image.to_json()) if image else None

# List all images of an image prompt
def list_images(shot_id):
    imagePromptImages = (
        Image.objects(shot_id=shot_id, is_deleted__ne=True)
    )
    return json.loads(imagePromptImages.to_json())

# Create a new image
def create_image(shot_id, blob_url):
    image = Image(
            shot_id=shot_id,
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

def generate_images(shot_id):
    """
    Generates images for a given image prompt and creates them in the system.
    """
    shot = get_shot(shot_id)
    
    # Placeholder for image generation logic
    # This function should call an AI service to generate images based on the shot_id
    # For now, we will return a list of created image IDs as a placeholder
    generated_image_ids = []

    base64image = generate_image_ai(shot["image_prompt"])

    # todo: Handle Error cases
    if not base64image:
        print(f"Image generation failed for shot_id: {shot_id}")
        return generated_image_ids

    image_bytes = base64.b64decode(base64image)
    
    blob_url = upload_image_to_storage(image_bytes, f"{shot_id}.jpg")
    
    image_id = create_image(shot_id, blob_url)
    if image_id:
        generated_image_ids.append(image_id)
    
    return generated_image_ids

def upload_image_to_storage(image_bytes, image_name):
    """
    Copies an image to a specified storage service.
    This function should implement the logic to copy the image to the desired storage service.
    """
    # Get Cloudflare R2 credentials and endpoint from environment variables
    r2_access_key = os.getenv("R2_ACCESS_KEY_ID")
    r2_secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
    r2_bucket = os.getenv("R2_BUCKET_NAME")
    r2_endpoint = os.getenv("R2_ENDPOINT_URL")
    r2_object_access_url = os.getenv("R2_OBJECT_ACCESS_URL")

    # Create a boto3 client for S3-compatible storage (Cloudflare R2)
    s3_client = boto3.client(
        "s3",
        endpoint_url=r2_endpoint,
        aws_access_key_id=r2_access_key,
        aws_secret_access_key=r2_secret_key,
        region_name="auto"
    )

    # Upload the image bytes to the R2 bucket
    s3_client.upload_fileobj(BytesIO(image_bytes), r2_bucket, image_name)

    # Construct the public URL (assuming public bucket)
    blob_url = f"{r2_object_access_url}/{image_name}"

    return blob_url