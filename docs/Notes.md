# Django
## Features
- Data Model Layer
- Admin Interface
- Template Language
- URL Mapping
- Forms
- Packages
- User Authentication
- HTTP Session Handling
- Caching
- Internationalization

## Django Concepts
1. **Django Apps**
- Organizes your code into subprojects
- Adds structure to your project, how you do that is upto you
- Apps can also be shared with others as plugins
- Files in Django Apps :

    1. **models.py** - Contains Data Structure of Model. Each class in model.py define a db table.
    2. **views.py** - Defines what happens when a page is visited.
    3. **urls.py** - Contains URL Patterns, Contains list of Paths
    4. **settings.py** - contains various settings such as db conn strings, third party packages settings etc.
    5. **asgi.py and wsgi.py** - For deploying to production.

2. **Django packages**
- External Packages to support more functionality in Django such as React Package etc.
3. 

# Mongo Db
# Mongo Engine
# Testing
# MongoMock
# DotEnv
# Celery
## Calling Tasks from another task
```
from celery import chain

@app.task
def generate_all(idea):
    """
    Generate script -> scenes -> shots asynchronously.
    """
    print("Generating all ...")

    # Chain the tasks
    workflow = chain(
        generate_script.s(idea),           # Step 1
        generate_scenes.s(),               # Step 2
    )

    # Execute the workflow
    result = workflow.apply_async()

    # Wait for script and scenes to complete
    script_and_scenes = result.get()

    script, scenes = script_and_scenes if isinstance(script_and_scenes, tuple) else (None, script_and_scenes)

    # Now generate shots for each scene in parallel
    shot_tasks = [generate_shots.delay(scene) for scene in scenes]

    shots = [shot.get() for shot in shot_tasks]

    print("All generated successfully!")

    return {
        "script": script,
        "scenes": scenes,
        "shots": shots
    }
```

In above example chain is used to chain two tasks and loop is used to fire parallel tasks (generate_shots) and another loop is used to wait for parallel tasks to finish execution using shot.get()
## Problem with get()
Get() is blocking 


# Python 
## Summary: Blocking vs Non-Blocking and Asynchronous Execution in Python
1. Blocking vs Non-Blocking Calls
    • Blocking call: Halts program execution until the operation completes (e.g., reading a large file).
    • Non-blocking call: Starts an operation and immediately returns control to the program, allowing other work to continue (e.g., asynchronous network request).
    Key idea: Non-blocking improves efficiency by letting the CPU handle other tasks while waiting for slow operations.

2. Why async def is Needed
    • In Python, the await keyword can only be used inside an async def function.
    • async def marks a function as asynchronous, allowing it to pause at await points and yield control back to the event loop.

3. What Happens During await?
    • When a function hits await, it suspends itself and hands control back to the event loop.
    • The event loop can:
        ○ Run other pending tasks (in the same program),
        ○ Or the CPU can switch to another program altogether.
    • Thus, await does not block the CPU — only that specific coroutine.

4. Example: Running Two Async Functions Together
    • We extended the process_data example with another independent async function, process_data_b.
    • Using asyncio.gather(process_data(), process_data_b()), both run independently and concurrently in the same event loop.
Code Sketch:
async def process_data():
    task1 = asyncio.create_task(fetch_data(...))
    task2 = asyncio.create_task(fetch_data(...))
    print("Other work...")
    result1 = await task1
    result2 = await task2
async def process_data_b():
    await asyncio.sleep(1)
    print("process_data_b done")
async def main():
    await asyncio.gather(process_data(), process_data_b())
asyncio.run(main())

5. Takeaways
    • Async programming keeps your program responsive and efficient.
    • Non-blocking operations let multiple tasks progress without waiting on each other unnecessarily.
    • The event loop ensures smooth task switching without manual thread management.

## Hard Blocking vs Soft-blocking
Good question — because terms like soft blocking and hard blocking often come up, especially when people talk about concurrency, multiprocessing, or async programming.
Let’s break them down clearly:

Soft Blocking vs Hard Blocking

Type	Meaning	Example	Behavior
Hard Blocking	Code completely stops execution until the operation is finished. No other work can happen. CPU is stuck.	time.sleep(5)	Program is frozen. Processor is idle for 5 seconds.
Soft Blocking	Code yields control while waiting for an operation (like I/O). Program can do other work in the meantime.	await asyncio.sleep(5)	Event loop switches to other tasks during wait. CPU is free to work on something else.
Hard Blocking (Real Blocking)
Happens when a function holds up the thread completely.

CPU cannot use that thread for anything else until it’s done.

Example functions:

time.sleep(5) (sleeping the thread)

socket.recv() (waiting for network packet synchronously)

open().read() (waiting for file I/O synchronously)

Consequences:

Freezes your app temporarily.

Wastes CPU cycles (idle).

Reduces responsiveness.

🧠 Think:
Like standing at a closed shop, refusing to move until it opens. You’re wasting your time doing nothing.

Soft Blocking (Cooperative "Waiting")
Happens when a function pauses itself, but lets others use the thread (usually through an event loop).

CPU is free to do other work.

Example functions:

await asyncio.sleep(5)

await fetch_data()

await async_db_query()

Consequences:

Increases concurrency without needing real threads.

Keeps app responsive.

Efficient use of CPU.

🧠 Think:
Like taking a token at a busy restaurant and going shopping until your number is called — no time wasted!

# NextJS
## Create-Next-App tool
Cmd for this tool

npx create-next-app@latest <appFolderName>

Your app code will be created inside a folder appFolderName
Prompts while running this tool

You will be prompted to choose the following:

1.TypeScript or JavaScript
TypeScript: Adds static typing to JavaScript, making the code more robust and maintainable.
2. ESLint
ESLint is a tool for identifying and fixing problems in your JavaScript/TypeScript code.
3. Tailwind CSS
Tailwind CSS is a utility-first CSS framework that provides pre-built classes for styling components.
4. src/ directory
Enabling the src/ directory structure keeps the root directory cleaner and more organized:
5. Experimental app directory/ App Router
Next.js 13 introduced a new app/ directory that leverages the latest React Server Components and the new routing system.
6. Import alias
Import Alias allows you to define custom paths for imports instead of using relative paths.

## globals.css
Please read the file inline comments
This file is used to set some basic settings such as background color, text color, font etc.

# Runpod
## Serverless

### Endpoints
An endpoint is the access point for your Serverless application. It provides a URL where users or applications can send requests to run your code. Each endpoint can be configured with different compute resources, scaling settings, and other parameters to suit your specific needs.

### Workers
Workers are the container instances that execute your code when requests arrive at your endpoint. Runpod automatically manages worker lifecycle, starting them when needed and stopping them when idle to optimize resource usage.

Each worker can use one or more GPUs for it's work.
When a request is received, it waits on queue and workers can pick up requests and work on them using one or more GPUs each.

### Handler functions
Handler functions are the core of your Serverless application. These functions define how a worker processes incoming requests and returns results. They follow a simple pattern:
```
import runpod  # Required

def handler(event):
    # Extract input data from the request
    input_data = event["input"]
    
    # Process the input (replace this with your own code)
    result = process_data(input_data)
    
    # Return the result
    return result

runpod.serverless.start({"handler": handler})  # Required
```


# Cloudfare R2 
boto3 - The AWS Python SDK for AWS S3 storage service which also supports Cloudfare R2
boto3 code examples for Cloudfare R2
https://developers.cloudflare.com/r2/examples/aws/boto3/

