# First import the Celery app instance from the mycelerymodule
from mycelerymodule import app
import time
from celery import chain, chord, group

# Use this app instance to register tasks

@app.task
def adder(x, y):
    """
    A simple task that adds two numbers.
    """
    return x + y

@app.task
def multiply(x, y):
    """
    A simple task that multiplies two numbers.
    """
    return x * y


@app.task(bind=True)
def hello(self, a, b):
    time.sleep(3)
    self.update_state(state="PROGRESS", meta={'progress': 50})
    time.sleep(3)
    self.update_state(state="PROGRESS", meta={'progress': 90})
    time.sleep(3)
    return 'hello world: %i' % (a+b)

@app.task
def print_message(message):
    """
    A simple task that prints a message.
    """
    print(message)
    return message

@app.task
def generate_all(idea):
    """
    A simple task that simulates generating a script, scenes, and shots.
    """
    # print("Generating all ...")
    # script = generate_script(idea)
    # scenes = generate_scenes(script)
    # shots = [generate_shots(scene) for scene in scenes]
    # print("All generated successfully!")
    # return {
    #     "script": script,
    #     "scenes": scenes,
    #     "shots": shots
    # }

    print("Generating all ...")

    # Step 1: Generate script
    script_task = generate_script.s(idea)

    # Step 2: Generate scenes from script
    scenes_task = generate_scenes.s()

    workflow = chain(
        script_task,
        scenes_task,
        fan_out_shots.s()
    )

    return workflow.apply_async()

@app.task
def fan_out_shots(scenes):
    """
    This task dynamically creates a chord to generate shots and collect them.
    """
    return chord(
        group(generate_shots.s(scene) for scene in scenes),
        collect_results.s()
    ).apply_async()

@app.task
def collect_results(shots):
    """
    Collect the shots after parallel generation.
    """
    print("Collecting all results...")
    print(f"Shots: {shots}")
    return {
        "shots": shots
    }

@app.task
def generate_script(idea):
    """
    A simple task that simulates script generation.
    """
    print("Generating script from idea ...")
    print(f"Idea: {idea}")
    # Simulate a long-running task
    time.sleep(5)
    print("Script generated successfully!")
    return "Once upon a time, there was a script"

@app.task
def generate_scenes(script):
    """
    A simple task that simulates scene generation from a script.
    """
    print("Generating scenes from script...")
    print(f"Script: {script}")
    time.sleep(5)
    print("Scenes generated successfully!")
    return ["Alpha", "Beta", "Gamma"]

@app.task
def generate_shots(scene):
    """
    A simple task that simulates shot generation from a scene.
    """
    print("Generating shots from scene...")
    print(f"Scene: {scene}")
    time.sleep(5)
    print("Shots generated successfully!")
    return [f"{scene} 1", f"{scene} 2", f"{scene} 3"]


