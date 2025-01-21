from mongoengine import EmbeddedDocument, fields
from shots.models import Shot

# mongoengine model for the Scene
class Scene(EmbeddedDocument):
    content = fields.StringField(required=True)
    shots = fields.ListField(fields.EmbeddedDocumentField(Shot))
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    is_deleted = fields.BooleanField(default=False)