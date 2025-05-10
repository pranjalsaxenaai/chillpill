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
 