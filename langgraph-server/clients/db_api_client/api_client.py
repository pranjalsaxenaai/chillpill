import requests
import os
from typing import Dict, Any, Optional

class APIClient:
    """Client for communicating with the Django backend API."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout: int = 30):
        """
        Initialize the API client.
        
        Args:
            base_url: The base URL of the backend API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = {
            "Content-Type": "application/json",
        }
    
    def set_auth_token(self, token: str) -> None:
        """Set the authentication token for subsequent requests."""
        self.headers["Authorization"] = f"Bearer {token}"
    
    # ============ POST Methods ============
    def post(self, endpoint: str, data: Dict[str, Any], token: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a POST request to the API.
        
        Args:
            endpoint: The API endpoint (e.g., "/api/scenes")
            data: The data to send in the request body
            token: Optional authentication token (if not already set)
        
        Returns:
            The JSON response from the API
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        headers = self.headers.copy()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, json=data, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            print(response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error posting to {url}: {e}")
            raise
    
    # ============ GET Methods ============
    def get(self, endpoint: str, params: Optional[Dict[str, str]] = None, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a GET request to the API.
        
        Args:
            endpoint: The API endpoint (e.g., "/api/projects")
            params: Optional query parameters
            token: Optional authentication token (if not already set)
        
        Returns:
            The JSON response from the API
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        headers = self.headers.copy()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting from {url}: {e}")
            raise
    
    # ============ PUT Methods ============
    def put(self, endpoint: str, data: Dict[str, Any], token: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a PUT request to the API.
        
        Args:
            endpoint: The API endpoint
            data: The data to send in the request body
            token: Optional authentication token (if not already set)
        
        Returns:
            The JSON response from the API
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        headers = self.headers.copy()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.put(url, json=data, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error putting to {url}: {e}")
            raise
    
    # ============ Helper Methods ============
    def health_check(self) -> bool:
        """Check if the API is reachable."""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=self.timeout)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False


# Singleton instance for easy access
api_client = APIClient()
