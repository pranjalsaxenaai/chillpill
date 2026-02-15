import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import dotenv

dotenv.load_dotenv()

class TokenIssuer:
    """
    Issues Google ID tokens for service-to-service (S2S) authentication.
    Uses a Google Service Account JSON file to generate OIDC tokens.
    """

    def __init__(self, sa_json_path: str = None, target_audience: str = None):
        """
        Initialize TokenIssuer with service account credentials.

        Args:
            sa_json_path (str): Path to Google Service Account JSON file.
                               Defaults to GOOGLE_SERVICE_ACCOUNT_JSON env var.
            target_audience (str): Target audience for the ID token (typically API URL).
                                  Defaults to GOOGLE_OIDC_AUDIENCE env var.

        Raises:
            ValueError: If required paths/audience are not provided or files don't exist.
        """
        self.sa_json_path = sa_json_path or os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        self.target_audience = target_audience or os.getenv("API_BASE_URL")

        if not self.sa_json_path:
            raise ValueError(
                "Service account JSON path not provided. "
                "Set GOOGLE_SERVICE_ACCOUNT_JSON env var or pass sa_json_path."
            )
        if not os.path.exists(self.sa_json_path):
            raise FileNotFoundError(f"Service account file not found: {self.sa_json_path}")
        if not self.target_audience:
            raise ValueError(
                "Target audience not provided. "
                "Set GOOGLE_OIDC_AUDIENCE env var or pass target_audience."
            )

        self._credentials = None

    def _load_credentials(self):
        """Lazily load service account credentials."""
        if self._credentials is None:
            self._credentials = service_account.IDTokenCredentials.from_service_account_file(
                self.sa_json_path,
                target_audience=self.target_audience,
            )
            print("Loaded service account credentials for audience:", self.target_audience)
            print(self._credentials.token)
        return self._credentials

    def get_id_token(self) -> str:
        """
        Get a fresh ID token from the service account.

        Returns:
            str: A valid Google OIDC ID token signed by the service account.

        Raises:
            Exception: If token generation or refresh fails.
        """
        creds = self._load_credentials()

        # Refresh the token from google auth server
        # Potential perf improvement: cache the token and its expiry
        creds.refresh(Request())
        return creds.token

    def __repr__(self) -> str:
        return f"TokenIssuer(audience='{self.target_audience}')"