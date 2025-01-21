from mongoengine import Document, fields
from scenes.models import Scene

# mongoengine model for the script
class Script(Document):
    content = fields.StringField(required=True)
    scenes = fields.ListField(fields.EmbeddedDocumentField(Scene))
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    is_deleted = fields.BooleanField(default=False)