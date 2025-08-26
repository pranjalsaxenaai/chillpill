# All API requests will go through this authentication class
# This class verifies Google ID tokens for authentication
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import os

class GoogleUser:
    def __init__(self, email, name, given_name, family_name):
        self.email = email
        self.name = name
        self.given_name = given_name
        self.family_name = family_name
        self.is_authenticated = True

class GoogleIDTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Missing or invalid Authorization header')

        token = auth_header.split(' ')[1]
        try:
            # Fetch Google client ID from environment variable
            CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            #print(idinfo)

            user_email = idinfo.get("email")
            user_name = idinfo.get("name")
            user_given_name = idinfo.get("given_name")
            user_family_name = idinfo.get("family_name")
            if not user_email:
                raise AuthenticationFailed('Invalid Google ID token: No email found')
            # Return your custom user type
            return (GoogleUser(user_email, user_name, user_given_name, user_family_name), None)
        except Exception:
            raise AuthenticationFailed('Invalid Google ID token')