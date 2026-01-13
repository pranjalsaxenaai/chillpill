from dataclasses import dataclass, field
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field
from typing_extensions import TypedDict



@dataclass
class Shot:
    image_prompt: str

@dataclass
class Scene:
    scene_index: int
    scene_description: str
    shots: List[Shot] = field(default_factory=list)

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
    # Structure Essentials
    input_idea: Optional[str] = None
    script: Optional[str] = None
    script_title: Optional[str] = None
    scenes: Annotated[List[Scene], fill_scenes_by_index_reducer] = Field(default_factory=list)

class ShotGenerationState(TypedDict):
    scene: Scene
