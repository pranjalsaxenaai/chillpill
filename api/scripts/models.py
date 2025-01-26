from mongoengine import Document, fields

# mongoengine model for the script
class Script(Document):
    content = fields.StringField(required=True)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    is_deleted = fields.BooleanField(default=False)