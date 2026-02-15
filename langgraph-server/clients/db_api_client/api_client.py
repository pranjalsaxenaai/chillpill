import requests
import aiohttp
import asyncio
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class APIClient:
    """
    HTTP client supporting both sync and async requests.
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
    
    # ============ Sync Methods ============
    
    def post(
        self,
        endpoint: str,
        data: Dict[str, Any],
        token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Synchronous POST request."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(token)
        
        try:
            response = requests.post(
                url,
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"POST {url} failed: {e}")
            raise
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        token: Optional[str] = None
    ) -> requests.Response:
        """Synchronous GET request."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(token)
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"GET {url} failed: {e}")
            raise
    
    def put(
        self,
        endpoint: str,
        data: Dict[str, Any],
        token: Optional[str] = None
    ) -> requests.Response:
        """Synchronous PUT request."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(token)
        
        try:
            response = requests.put(
                url,
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"PUT {url} failed: {e}")
            raise
    
    # ============ Async Methods ============
    
    async def post_async(
        self,
        endpoint: str,
        data: Dict[str, Any],
        token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Asynchronous POST request."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(token)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"POST {url} failed: {e}")
            raise
    
    async def get_async(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Asynchronous GET request."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(token)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"GET {url} failed: {e}")
            raise
    
    async def put_async(
        self,
        endpoint: str,
        data: Dict[str, Any],
        token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Asynchronous PUT request."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(token)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    url,
                    json=data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"PUT {url} failed: {e}")
            raise
    
    # ============ Helper Methods ============
    
    def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
        """Get HTTP headers with optional auth token."""
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers
