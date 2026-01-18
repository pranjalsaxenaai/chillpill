from langgraph_sdk import get_client
from typing import Dict, Any, Optional, TypedDict
import logging
import os
from dotenv import load_dotenv

# Import TokenIssuer from your auth module
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'langgraph-server'))
from auth.token_issuer import TokenIssuer

load_dotenv()
logger = logging.getLogger(__name__)

class LangGraphClient:
    """
    Client for interacting with LangGraph server.
    Handles authentication using service account tokens.
    """
    
    def __init__(
        self,
        langgraph_url: Optional[str] = None,
        token_issuer: Optional[TokenIssuer] = None,
        sa_json_path: Optional[str] = None,
        target_audience: Optional[str] = None
    ):
        """
        Initialize LangGraph client with authentication.
        
        Args:
            langgraph_url: URL of LangGraph server (default: from env)
            token_issuer: TokenIssuer instance (optional, will create if not provided)
            sa_json_path: Path to service account JSON file
            target_audience: Target audience for OIDC token
        """
        self.langgraph_url = langgraph_url or os.getenv("LANGGRAPH_SERVER_URL", "http://127.0.0.1:2024")
        
        # Initialize token issuer
        if token_issuer:
            self.token_issuer = token_issuer
        else:
            self.token_issuer = TokenIssuer(
                sa_json_path=sa_json_path,
                target_audience=target_audience
            )
        
        # Initialize LangGraph SDK client
        self.client = get_client(
            url=self.langgraph_url,
            headers={"Authorization": f"Bearer {self.token_issuer.get_id_token()}"}
        )

        logger.info(f"LangGraphClient initialized with URL: {self.langgraph_url}")
    
    def get_run(self, run_id: str) -> Dict[str, Any]:
        """
        Get the details of a graph run.
        
        Args:
            run_id: ID of the run to check
        
        Returns:
            Run details information
        """
        logger.info(f"Fetching run details: {run_id}")

        try:
            run = self.client.runs.get(run_id=run_id)
            return run
        
        except Exception as e:
            logger.error(f"Failed to get run details {run_id}: {e}", exc_info=True)
            raise
    
    def create_run(
        self,
        graph_name: str,
        input_data: Dict[str, Any],
        thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new run without waiting for completion.
        
        Args:
            graph_name: Name of the graph to run
            input_data: Input data for the graph
            thread_id: Persistent state thread ID, if not provided a new thread will be created

        Returns:
            Run for tracking - Includes run_id, thread_id and other metadata
        """
        logger.info(f"Creating run for graph: {graph_name}")
        
        try:
            config = {}
            if thread_id is None:
                thread_id = self.client.threads.create()['thread_id']

            config["configurable"] = {"thread_id": thread_id}
            
            run = self.client.runs.create(
                graph_id=graph_name,
                input=input_data,
                config=config
            )

            logger.info(f"Run created: {run['run_id']}")
            return run
        except Exception as e:
            logger.error(f"Failed to create run: {e}", exc_info=True)
            raise
    
    def health_check(self) -> bool:
        """
        Check if LangGraph server is healthy.
        
        Returns:
            True if server is healthy, False otherwise
        """
        logger.info("Performing LangGraph server health check")
        
        try:
            graphs = self.client.graphs.list()
            logger.info("LangGraph server is healthy")
            return True
        except Exception as e:
            logger.error(f"LangGraph server health check failed: {e}")
            return False


# ============ Example Usage ============

if __name__ == "__main__":
    # Option 1: Using environment variables
    client = LangGraphClient()
    
    # Option 2: With explicit configuration
    token_issuer = TokenIssuer(
        sa_json_path="/path/to/service-account.json",
        target_audience="https://langgraph.yourdomain.com"
    )
    client = LangGraphClient(
        langgraph_url="http://localhost:2024",
        token_issuer=token_issuer
    )
    
    # Check server health
    if client.health_check():
        print("✅ LangGraph server is healthy")
    
    # List available graphs
    graphs = client.list_graphs()
    print(f"Available graphs: {graphs}")
    
    # Invoke a graph
    result = client.invoke_graph(
        graph_name="story_generation",
        input_data={
            "project_id": "proj_123",
            "input_idea": "A magical adventure"
        }
    )
    print(f"Result: {result}")
    
    # Stream graph execution
    print("\nStreaming graph execution:")
    for event in client.stream_graph(
        graph_name="story_generation",
        input_data={"project_id": "proj_123"}
    ):
        print(f"Event: {event}")


