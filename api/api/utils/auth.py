# All API requests will go through this authentication class
# This class verifies Google ID tokens for authentication
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api import settings

# Custom user class to hold Authenticated Google user information.
class GoogleUser:
    def __init__(self, email, name, given_name, family_name):
        self.email = email
        self.name = name
        self.given_name = given_name
        self.family_name = family_name
        self.is_authenticated = True # signals to DRF that the user is authenticated
        self.principal_type = "user"

class ServicePrincipal:
    def __init__(self, service: str, email: str):
        self.service = service                  # e.g. "langgraph"
        self.email = email                        # service account email
        self.is_authenticated = True
        self.principal_type = "service"

class GoogleIDTokenAuthentication(BaseAuthentication):
    """
    Accepts:
      1) Google user ID tokens (Google Sign-In)  -> verified against GOOGLE_CLIENT_ID
      2) Google OIDC ID tokens for S2S           -> verified against GOOGLE_OIDC_AUDIENCE
    Distinguishes service accounts by email domain and allowlist.
    """
    def authenticate(self, request):

        # Extracting token from Auth Header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Missing or invalid Authorization header')

        token = auth_header.split(' ')[1]

        # Check if token is present, else raise an error
        if not token:
            raise AuthenticationFailed("Missing bearer token")

        # Fetch Google public cert
        google_public_cert = google_requests.Request()

        
        try:
            # Fetch Google client ID for User Auth and Audience for App Auth
            GOOGLE_CLIENT_ID = getattr(settings, "GOOGLE_CLIENT_ID", None)
            GOOGLE_OIDC_AUDIENCE = getattr(settings, "GOOGLE_OIDC_AUDIENCE", None)

            idinfo = None

            # Check if the token is for App Auth
            try:
                idinfo = id_token.verify_oauth2_token(token, google_public_cert, GOOGLE_OIDC_AUDIENCE)
            
            except Exception as e:
                print(e)
                idinfo = None
                # If OIDC verification fails, it might be a user token
                pass

            # Check for user token
            if idinfo is None:
                 try:
                     idinfo = id_token.verify_oauth2_token(token, google_public_cert, GOOGLE_CLIENT_ID)
                 except Exception:
                     raise AuthenticationFailed("Invalid Google ID token")

            # Checking email claim
            email = idinfo.get("email")
            if not email:
                raise AuthenticationFailed("Token missing email claim")

            # Detect service account token
            is_service_account = email.endswith(".gserviceaccount.com")

            # If service account token
            if is_service_account:
                allowed = getattr(settings, "LANGGRAPH_SERVICE_ACCOUNT_EMAILS", set())
                if allowed and email not in allowed:
                    raise AuthenticationFailed("Unauthorized service account")

                # Identify which service this is (you can map by email)
                service_name = "langgraph"  # or map based on email
                return (ServicePrincipal(service=service_name, email=email), None)

            # If Google User Account
            # Check is email is verified or not
            email_verified = idinfo.get("email_verified", False)
            if not email_verified:
                raise AuthenticationFailed('Email not verified in Google ID token')

            return (
                GoogleUser(
                    email=email,
                    name=idinfo.get("name"),
                    given_name=idinfo.get("given_name"),
                    family_name=idinfo.get("family_name"),
                ),
                None,
            )
        
        except Exception:
            raise AuthenticationFailed('Unknown Error while validating Google ID token')