from mongoengine import Document, fields

# mongoengine model for the Scene
class Scene(Document):
    script_id = fields.StringField(required=True)
    content = fields.StringField(required=True)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    is_deleted = fields.BooleanField(default=False)