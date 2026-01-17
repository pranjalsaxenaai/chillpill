from langgraph.graph import StateGraph, END
from typing import Annotated
from operator import add
from contracts.states import StoryState, Scene
from typing import List
from nodes import ai_nodes, db_nodes
from edges import fanout_to_shots
import dotenv

dotenv.load_dotenv()


def merge_scenes_reducer(left: List[Scene], right: List[Scene]) -> List[Scene]:
    """Reducer: merge updated scenes from parallel fanout calls."""
    if not left:
        return right
    if not right:
        return left
    # Create a dict of scenes by index for O(1) lookup
    scenes_dict = {scene.scene_index: scene for scene in left}
    # Update with any new/modified scenes from right
    for scene in right:
        scenes_dict[scene.scene_index] = scene
    # Return sorted by index
    return sorted(scenes_dict.values(), key=lambda s: s.scene_index)

def build_story_graph():
    g = StateGraph(StoryState)

    # Add AI nodes
    g.add_node("generate_script", ai_nodes.generate_script)
    g.add_node("generate_scenes", ai_nodes.generate_scenes)
    g.add_node("generate_shots", ai_nodes.generate_shots)

    # Add DB Nodes
    g.add_node("store_script", db_nodes.store_script_node)

    g.add_node("join", lambda state: state)

    # Set entry point and edges
    g.set_entry_point("generate_script")
    g.add_edge("generate_script", "store_script")
    g.add_edge("store_script", "generate_scenes")
    # Use conditional edges to fanout to generate_shots for each scene
    g.add_conditional_edges(
        "generate_scenes",
        fanout_to_shots,
        ["generate_shots"]
    )
    g.add_edge("generate_shots", "join")
    g.add_edge("join", END)

    return g.compile()

graph = build_story_graph()