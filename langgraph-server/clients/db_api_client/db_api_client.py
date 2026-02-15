import asyncio
import aiohttp
from .api_client import APIClient
from auth.token_issuer import TokenIssuer
import os
import logging

logger = logging.getLogger(__name__)

class DBAPIClient:
    """
    Async API client for Django backend.
    Supports both sync and async operations.
    """
    
    def __init__(self, token_issuer: TokenIssuer):
        self.client = APIClient(base_url=os.getenv("API_BASE_URL"))
        self.token_issuer = token_issuer
        self._session: aiohttp.ClientSession = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Get or create aiohttp session for async requests.
        
        Returns:
            aiohttp.ClientSession: Reusable HTTP session
        """
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    # ============ Async Methods ============
    
    async def create_script_async(self, project_id: str, script_data: str) -> dict:
        """
        Async: Create a script.
        
        Args:
            project_id: Project ID
            script_data: Script content
        
        Returns:
            API response with script ID
        """
        try:
            logger.info(f"Creating script for project: {project_id}")
            
            response = await self.client.post_async(
                "/api/scripts",
                data={"script": script_data, "project_id": project_id},
                token= await self.token_issuer.get_id_token_async()
            )
            logger.info(f"Script created: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to create script: {e}", exc_info=True)
            raise
    
    async def create_scene_async(self, script_id: str, scene_data: str) -> dict:
        """
        Async: Create a scene.
        
        Args:
            script_id: Script ID
            scene_data: Scene object
        
        Returns:
            API response with scene ID
        """
        try:
            logger.info(f"Creating scene for script: {script_id}")
            
            response = await self.client.post_async(
                "/api/scenes",
                data={"scene": scene_data, "script_id": script_id},
                token=await self.token_issuer.get_id_token_async()
            )
            logger.info(f"Scene created: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to create scene: {e}", exc_info=True)
            raise
    
    async def create_shot_async(self, scene_id: str, shot_data) -> dict:
        """
        Async: Create a shot.
        
        Args:
            scene_id: Scene ID
            shot_data: Shot object
        
        Returns:
            API response with shot ID
        """
        try:
            logger.info(f"Creating shot for scene: {scene_id}")
            
            response = await self.client.post_async(
                "/api/shots",
                data={"shot": shot_data, "scene_id": scene_id},
                token=await self.token_issuer.get_id_token_async()
            )
            logger.info(f"Shot created: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to create shot: {e}", exc_info=True)
            raise
    
    async def get_script_async(self, script_id: str) -> dict:
        """
        Async: Get a script.
        
        Args:
            script_id: Script ID
        
        Returns:
            Script data
        """
        try:
            logger.info(f"Fetching script: {script_id}")
            
            response = await self.client.get_async(
                f"/api/scripts/{script_id}/",
                token=await self.token_issuer.get_id_token_async()
            )
            return response
        except Exception as e:
            logger.error(f"Failed to get script: {e}", exc_info=True)
            raise
    
    async def update_project_async(
        self,
        project_id: str,
        title: str,
        description: str,
        script_id: str
    ) -> dict:
        """
        Async: Update a project.
        
        Args:
            project_id: Project ID
            title: Project title
            description: Project description
            script_id: Associated script ID
        
        Returns:
            Updated project data
        """
        try:
            logger.info(f"Updating project: {project_id}")
            
            response = await self.client.put_async(
                f"/api/projects/{project_id}/",
                data={
                    "project_title": title,
                    "project_desc": description,
                    "script_id": script_id
                },
                token=await self.token_issuer.get_id_token_async()
            )
            logger.info(f"Project updated: {project_id}")
            return response
        except Exception as e:
            logger.error(f"Failed to update project: {e}", exc_info=True)
            raise
    
    # ============ Sync Methods (Backward Compatibility) ============
    
    def create_script(self, project_id: str, script_data: str) -> dict:
        """Sync wrapper for create_script_async."""
        return asyncio.run(self.create_script_async(project_id, script_data))
    
    def create_scene(self, script_id: str, scene_data) -> dict:
        """Sync wrapper for create_scene_async."""
        return asyncio.run(self.create_scene_async(script_id, scene_data))
    
    def create_shot(self, scene_id: str, shot_data) -> dict:
        """Sync wrapper for create_shot_async."""
        return asyncio.run(self.create_shot_async(scene_id, shot_data))
    
    def get_script(self, script_id: str) -> dict:
        """Sync wrapper for get_script_async."""
        return asyncio.run(self.get_script_async(script_id))
    
    def update_project(
        self,
        project_id: str,
        title: str,
        description: str,
        script_id: str
    ) -> dict:
        """Sync wrapper for update_project_async."""
        return asyncio.run(
            self.update_project_async(project_id, title, description, script_id)
        )


# ============ Singleton Instance ============
token_issuer = TokenIssuer()
db_api_client = DBAPIClient(token_issuer=token_issuer)