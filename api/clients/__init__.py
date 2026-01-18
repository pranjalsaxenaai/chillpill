from .langgraph_client import LangGraphClient
import logging

logger = logging.getLogger(__name__)

# ============ Singleton Instance ============
_langgraph_client_instance = None

def get_langgraph_client() -> LangGraphClient:
    """
    Get the singleton LangGraph client instance.
    Creates it on first call, reuses it on subsequent calls.
    
    Returns:
        LangGraphClient: Singleton instance
    """
    global _langgraph_client_instance
    
    if _langgraph_client_instance is None:
        logger.info("Initializing singleton LangGraph client")
        _langgraph_client_instance = LangGraphClient()
    
    return _langgraph_client_instance

def reset_langgraph_client():
    """
    Reset the singleton instance (useful for testing).
    """
    global _langgraph_client_instance
    _langgraph_client_instance = None
    logger.info("LangGraph client instance reset")

# Export for easy importing
__all__ = ['get_langgraph_client', 'reset_langgraph_client', 'LangGraphClient']