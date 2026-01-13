
from langchain_core.messages import HumanMessage, SystemMessage
from contracts.structured_output_schemas import ScenesOutput, ImagesOutput
from contracts.states import StoryState, ShotGenerationState, Shot, Scene
from llm import llm_text, llm_structured
import prompts


def generate_script(state: StoryState) -> StoryState:
    idea = state.input_idea
    script = llm_text(prompts.SCRIPT_GENERATOR_HUMAN_PROMPT.format(idea=idea))
    state.script = script
    return state

def generate_scenes(state: StoryState) -> StoryState:

    scenesRunOutput = llm_structured(
        [SystemMessage(content=prompts.SCENE_GENERATOR_SYSTEM_PROMPT),
        HumanMessage(content=prompts.SCENE_GENERATOR_HUMAN_PROMPT.format(script=state.script))],
        ScenesOutput
    )
    scenesList = sorted(scenesRunOutput.scenes, key=lambda x: x.scene_number)

    state.scenes = [Scene(scene_index=i, scene_description=scene.scene_description, shots=[]) for i, scene in enumerate(scenesList)]
    return state


# for each scene, there will be multiple shots

def generate_shots(state: ShotGenerationState) -> StoryState:
    scene = state["scene"]
    system_prompt = SystemMessage(content=prompts.SHOT_GENERATOR_SYSTEM_PROMPT)
    prompt = HumanMessage(content=prompts.SHOT_GENERATOR_HUMAN_PROMPT.format(scene_description=scene.scene_description))

    shotsRunOutput = llm_structured([system_prompt, prompt], ImagesOutput)
    sceneShotsList = sorted(shotsRunOutput.images, key=lambda x: x.image_number)
    scene.shots = [Shot(image_prompt=s.image_prompt) for s in sceneShotsList]
    return {"scenes": [scene]}