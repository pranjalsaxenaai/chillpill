from contracts import StoryState

from langgraph.types import Send

def fanout_to_shots(state: StoryState) -> list[Send]:
    return [Send("generate_shots", {"scene": scene}) for scene in state.scenes]