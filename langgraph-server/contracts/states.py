from dataclasses import dataclass, field
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field, PrivateAttr
from typing_extensions import TypedDict
from clients.db_api_client.db_api_client import DBAPIClient, db_api_client


@dataclass
class Shot:
    image_prompt: str

@dataclass
class Scene:
    scene_index: int
    scene_description: str
    shots: List[Shot] = field(default_factory=list)

@dataclass
class DBMetadata:
    project_id: str
    script_id: Optional[str] = None


def fill_scenes_by_index_reducer(left: List[Scene], right: List[Scene]) -> List[Scene]:
    """Reducer: merge updated scene from parallel fanout calls by index.
    
    Args:
        left: The current list of scenes
        right: A single-element list containing the updated scene
    
    Returns:
        Updated list of scenes with the new scene merged by index
    """
    if not left:
        return right
    if not right:
        return left
    
    # Get the single updated scene from right
    updated_scene = right[0]
    
    # Create a dict of scenes by index and update with the new scene
    scenes_dict = {scene.scene_index: scene for scene in left}
    scenes_dict[updated_scene.scene_index] = updated_scene
    
    # Return sorted by index
    return sorted(scenes_dict.values(), key=lambda s: s.scene_index)

class StoryState(BaseModel):
    # Story Data
    input_idea: Optional[str] = None
    script: Optional[str] = None
    script_title: Optional[str] = None
    scenes: Annotated[List[Scene], fill_scenes_by_index_reducer] = Field(default_factory=list)

    # DB Metadata
    db_metadata: DBMetadata = Field(default_factory=DBMetadata)

    # Callable Objects
    # Making this a PrivateAttr, so that it does not get serialized/deserialized for checkpointing
    _db_api_client: DBAPIClient = PrivateAttr(default_factory=lambda: db_api_client)
    
    @property
    def db_api_client(self) -> DBAPIClient:
        return self._db_api_client

class ShotGenerationState(TypedDict):
    scene: Scene
