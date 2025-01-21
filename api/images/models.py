from mongoengine import EmbeddedDocument, fields

# mongoengine model for the Image
class Image(EmbeddedDocument):
    blob_url = fields.StringField(required=True)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    is_deleted = fields.BooleanField(default=False)