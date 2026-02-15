
import asyncio
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Send
from contracts.structured_output_schemas import ScenesOutput, ImagesOutput
from contracts.states import StoryState, ShotGenerationState, Shot, Scene
from llm import llm_text, llm_structured
import prompts
from clients.db_api_client.db_api_client import db_api_client

class AINodes:
    @staticmethod
    def generate_script(state: StoryState) -> StoryState:
        idea = state.input_idea
        script = llm_text(prompts.SCRIPT_GENERATOR_HUMAN_PROMPT.format(idea=idea))
        state.script = script
        return state

    @staticmethod
    def generate_scenes(state: StoryState) -> StoryState:

        scenesRunOutput = llm_structured(
            [SystemMessage(content=prompts.SCENE_GENERATOR_SYSTEM_PROMPT),
            HumanMessage(content=prompts.SCENE_GENERATOR_HUMAN_PROMPT.format(script=state.script))],
            ScenesOutput
        )
        scenesList = sorted(scenesRunOutput.scenes, key=lambda x: x.scene_number)

        state.scenes = [Scene(scene_index=i, scene_description=scene.scene_description, shots=[]) for i, scene in enumerate(scenesList)]
        return state

    @staticmethod
    def generate_shots(state: ShotGenerationState) -> dict:
        scene = state["scene"]
        system_prompt = SystemMessage(content=prompts.SHOT_GENERATOR_SYSTEM_PROMPT)
        prompt = HumanMessage(content=prompts.SHOT_GENERATOR_HUMAN_PROMPT.format(scene_description=scene.scene_description))

        shotsRunOutput = llm_structured([system_prompt, prompt], ImagesOutput)
        sceneShotsList = sorted(shotsRunOutput.images, key=lambda x: x.image_number)
        scene.shots = [Shot(image_prompt=s.image_prompt) for s in sceneShotsList]
        return Send("store_shots", {"scene": scene})

class DBNodes:
    @staticmethod
    async def store_script_node(state: StoryState) -> StoryState:
        response = await db_api_client.create_script_async(state.db_metadata.project_id, state.script)
        print(response)
        state.db_metadata.script_id = response
        return state

    @staticmethod
    async def store_scenes_node(state: StoryState) -> StoryState:
        script_id = state.db_metadata.script_id
        scenes = state.scenes

        # Create all scene tasks
        tasks = [
            db_api_client.create_scene_async(script_id, scene.scene_description)
            for scene in scenes
        ]
        
        # Run all in parallel
        results = await asyncio.gather(*tasks)
        
        # Update scenes with db_ids
        for scene, response in zip(scenes, results):
            scene.db_id = response

        return state

    
    @staticmethod
    async def store_shots_node(state: dict) -> StoryState:
        scene = state["scene"]

        # Create all scene tasks
        tasks = [
            db_api_client.create_shot_async(scene.db_id, shot.image_prompt)
            for shot in scene.shots
        ]

        # Run all in parallel
        results = await asyncio.gather(*tasks)

        # Update shots with db_ids
        for shot, response in zip(scene.shots, results):
            shot.db_id = response

        return {"scenes": [scene]}

ai_nodes = AINodes()
db_nodes = DBNodes()