from mongoengine import Document, fields

# mongoengine model for the project
class Project(Document):
    user_email = fields.StringField(required=True)
    project_title = fields.StringField(required=True)
    project_desc = fields.StringField(required=True)
    script_id = fields.StringField(required=False)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    is_deleted = fields.BooleanField(default=False)