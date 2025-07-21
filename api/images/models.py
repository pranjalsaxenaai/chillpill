from mongoengine import Document, fields

# mongoengine model for the Image
class Image(Document):
    shot_id = fields.StringField(required=True)
    blob_url = fields.StringField(required=True)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    is_deleted = fields.BooleanField(default=False)