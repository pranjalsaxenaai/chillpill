
import re
from langgraph.types import Send
from langchain_core.messages import HumanMessage, SystemMessage
from contracts import StoryState, Scene, Shot, ShotGenerationState, ScenesOutput, ImagesOutput
from llm import llm_text, llm_structured


def generate_script(state: StoryState) -> StoryState:
    prompt = """
    You are a creative script writer. 
    Write a descriptive script for a short film on below idea:\n\n{idea}
    """
    #print(text)
    # naive parse: split lines starting with "-" or "•"
    idea = state.input_idea
    script = llm_text(prompt.format(idea=idea))
    state.script = script
    return state

def generate_scenes(state: StoryState) -> StoryState:
    system_prompt = SystemMessage(content="""
    **System / Instruction**
    You are a screenplay scene breaker + continuity editor for a movie-creation app.
Your job is to convert the provided script into a scene list with light elaboration (visuals, actions, setting, mood), while staying strictly faithful to the script.

**Core Rules (must follow)**

No contradictions: Nothing in any scene may conflict with any other scene or with the script.

No new plot: Do not invent major events, twists, characters, relationships, locations, or outcomes that are not implied by the script.

Allowed elaboration: You may add cinematic details that do not change meaning (environment, body language, lighting, pacing, background actions, camera suggestions).

Preserve facts: Names, timeline, places, motivations, injuries, items, and outcomes must remain consistent across all scenes.

Resolve ambiguity safely: If the script is ambiguous, choose the least-committal interpretation and keep details generic rather than making up specifics.

Continuity tracking: Maintain consistent: wardrobe, time-of-day progression, props, character knowledge (who knows what when), emotional states, and cause→effect.

Dialogue fidelity: If you include dialogue, quote it exactly from the script. Otherwise summarize dialogue beats without adding new lines.

Scene boundaries: Start a new scene when there is a change in location, time, major beat, or point-of-view focus.
                                  
**Process You Must Use Internally (don’t output this)**

First, extract all facts (characters, relationships, timeline hints, locations, props, objectives, constraints).

Second, segment the script into scene units.

Third, elaborate each scene with only “safe” details.

Fourth, run a continuity pass: ensure every scene aligns with all established facts and earlier scenes.
        
    """)

    prompt = """
    **Script Input**

Here is the full script content (use this as the only source of truth):

<<<SCRIPT_START
\n{script}\n
SCRIPT_END>>>
    """
    scenesRunOutput = llm_structured([system_prompt] + [HumanMessage(content=prompt.format(script=state.script))], ScenesOutput)
    scenesList = sorted(scenesRunOutput.scenes, key=lambda x: x.scene_number)

    state.scenes = [Scene(scene_index=i, scene_description=scene.scene_description, shots=[]) for i, scene in enumerate(scenesList)]
    return state


# for each scene, there will be multiple shots

def generate_shots(state: ShotGenerationState) -> StoryState:
    scene = state["scene"]
    system_prompt = SystemMessage(content="""
**System / Instruction**

You are a cinematic storyboard generator and image-prompt specialist.

Your task is to convert one completed scene into a sequence of consecutive images that, when viewed in order, visually tell the scene without contradiction.

You must strictly adhere to the scene content and maintain visual and narrative continuity across all images.

**Non-Negotiable Rules**

1. No new story content
    - Do NOT invent events, actions, characters, props, locations, or emotions not present or implied in the scene.

2. No contradictions
    - All images must be consistent with:
        - Scene facts
        - Character states
        - Props, wardrobe, injuries
        - Time of day, weather, location

3. Consecutive continuity
    - Images must form a chronological visual flow, not disconnected moments.

4. One moment per image
    - Each image represents a single frozen cinematic beat.

5. Character consistency
   - Physical appearance, clothing, posture, emotional state must evolve logically across images.

6. Safe elaboration only
    - You may add lighting, composition, framing, depth, and atmosphere
    - You may NOT add plot, dialogue, or symbolism that changes meaning

7. Image-friendly phrasing
   - Prompts must be suitable for diffusion-based image models (clear subject, environment, lighting, mood).
                                  
**Image Prompt Construction Rules**

Each image_prompt MUST include:
- Primary subject(s) (who or what)
- Action or posture
- Environment / setting
- Lighting
- Mood / emotion
- Camera framing (wide shot, medium shot, close-up, over-the-shoulder, etc.)
- Visual realism cues (cinematic, high detail, depth of field, film grain, etc.)

Each negative_prompt SHOULD block:
- Extra characters
- Wrong time of day
- Inconsistent clothing
- Text, subtitles, watermarks
- Stylized artifacts unless specified

**Internal Reasoning Process (do NOT output)**
- Identify key visual beats in the scene
- Select the minimum number of images needed to clearly tell the scene
- Order them strictly by time
- Lock character appearances early
- Verify every image against scene continuity
""")
    prompt = HumanMessage(content=f"""
    **Scene Input**

You will be given a single fully defined scene in structured or narrative form.

Use this scene as the only source of truth. 
<<<SCENE_START
    \n{scene.scene_description}\n
SCENE_END>>>
    """)
    shotsRunOutput = llm_structured([system_prompt, prompt], ImagesOutput)
    sceneShotsList = sorted(shotsRunOutput.images, key=lambda x: x.image_number)
    scene.shots = [Shot(image_prompt=s.image_prompt) for s in sceneShotsList]
    return {"scenes": [scene]}