import os
import asyncio
from langgraph_sdk import Auth
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

auth = Auth()

@auth.authenticate
async def authenticate(authorization: str | None) -> Auth.types.MinimalUserDict:
    # Require Bearer token
    if not authorization:
        raise Auth.exceptions.HTTPException(status_code=401, detail="Missing Authorization header")

    scheme, token = authorization.split(" ", 1)
    if scheme.lower() != "bearer":
        raise Auth.exceptions.HTTPException(status_code=401, detail="Expected Bearer token")

    try:
        google_public_cert = google_requests.Request()
        # Move blocking HTTP call to a thread to avoid blocking the event loop
        idinfo = await asyncio.to_thread(
            id_token.verify_oauth2_token,
            token,
            google_public_cert,
            os.getenv("GOOGLE_OIDC_AUDIENCE")
        )
        if idinfo is None:
            raise Auth.exceptions.HTTPException(status_code=401, detail="Invalid Google OIDC ID token")
    except Exception as e:
        print(e)
        raise Auth.exceptions.HTTPException(status_code=401, detail="Invalid Google ID token")

    email = idinfo.get("email")
    if not email:
        raise Auth.exceptions.HTTPException(status_code=401, detail="Invalid Google ID token")

    is_service_account = email.endswith(".gserviceaccount.com")
    if is_service_account:
        allowed = os.getenv("CHILLPILL_API_SERVICE_ACCOUNT_EMAILS", "").split(",")
        if allowed and email not in allowed:
            raise Auth.exceptions.HTTPException(status_code=401, detail="Unauthorized service account")

        # Identify which service this is (you can map by email)
        service_name = "chillpill-api"  # or map based on email
        return {"identity": service_name}   

    # Only allowing service accounts to access langgraph-server
    else:
        raise Auth.exceptions.HTTPException(status_code=401, detail="Unauthorized user")