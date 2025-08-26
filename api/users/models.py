from mongoengine import Document, fields

# mongoengine model for the project
class User(Document):
    user_email = fields.StringField(required=True)
    first_name = fields.StringField(required=True)
    last_name = fields.StringField(required=True)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    is_deleted = fields.BooleanField(default=False)