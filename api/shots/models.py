from mongoengine import Document, fields

# mongoengine model for the Scene
class Shot(Document):
    scene_id = fields.StringField(required=True)
    image_prompt = fields.StringField(required=True)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    is_deleted = fields.BooleanField(default=False)