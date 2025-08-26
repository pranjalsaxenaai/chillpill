
import json
import datetime
from users.models import User
from exceptions.resource_exceptions import ResourceConflictException, UnhandledResourceException


def get_user(email):
    user = User.objects(user_email = email, is_deleted__ne=True).first()
    return json.loads(user.to_json()) if user else None

def create_user(email, name, given_name, family_name):
    # checking if user already exists
    existing_user = User.objects(user_email=email, is_deleted__ne=True).first()
    if existing_user:
        raise ResourceConflictException()
    user = User(
            user_email=email,
            first_name=given_name,
            last_name=family_name,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now())
    try:
        user.save()
    except Exception as e:
        print(e)
        raise UnhandledResourceException()
    return str(user.id)