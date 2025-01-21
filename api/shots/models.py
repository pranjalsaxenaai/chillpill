from mongoengine import EmbeddedDocument, fields
from images.models import Image

# mongoengine model for the Scene
class Shot(EmbeddedDocument):
    image_prompt = fields.StringField(required=True)
    images = fields.ListField(fields.EmbeddedDocumentField(Image))
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    is_deleted = fields.BooleanField(default=False)