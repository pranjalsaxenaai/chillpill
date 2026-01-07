# All Assets Generation
1. The operations api controller is called with post request to start a new operation and the operation id is returned.
2. In the new operation, operations service firstly enqueues generate_script_task on celery.
3. Once, it completes, operations service fetches the script content returned from the generate_script_task and calls the generate_scenes_task, operations service subsequently calls generate_shots_task, generate_image_task etc. consecutively to create all assets.

4. 

# API 
## Scripting Elements
Scripts, Scenes, Shots, Images
### Services
Responsible to communicate with database
### AI Services
Responsible to generate required AI elements.

## User Management Elements
Users

## Working Elements
Operations
### Services
Manage Operations like running tasks etc.
### Tasks
Tasks for Cross Script Element operations such as generating Script using Script AI service and saving it in db using Script Service

# Data Flow
The langgraph will create the elements required for a project - Script, Scenes, Shot Image Prompts.
They will be stored in Mongo DB Database
APIs can read from the MongoDB when user reads the existing project resources.

Langgraph will call an API Webhook when run finishes and API will run the code to read the run output and persist resources in DB.
We are not using LongTerm memory of LangGraph for storing the data, because this data has a specific format which needs to be read by UI App thus needs to be of strict schema.

We can use LongTerm Langgraph memory for conversations but not for data to be presented in a deterministic UI.

# Role of Langgraph
Langgraph will be used to create resources but will be stateless.
Each langgraph run may persist data or memory within a run but this memory will not be used in future.
All resources once created will be saved in Mongo DB

In case of retries, the langgraph will be provided with required data in the input state to recreate resources.
Once resources are recreated, the revised resources will be written to mongo db.


# Draw.io Diagram Project 
https://app.diagrams.net/#G1xslzoI289Rjn3LVbVphtOdrvV7Rhdvk-#%7B%22pageId%22%3A%22_0wMtbdc3ramDyEH5_Cz%22%7D

