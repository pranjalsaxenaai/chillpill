# Objective
# Concepts
## Users
The app supports multiple users to login and manage their video projects. 
## Projects
One user can have multiple video projects. A project encapsulates all resources required to create one video.

## Scripts
A script is a part of a project. It is the full text script of the video consisting of all the parts of the video.

## Scenes
A Scene is a part of a script defining a set of events happening in a single place in the video such as a court room scene consisting of multiple shots showing argument between individuals.
You may use a scene as a logical group of shots for any other purpose.

## Shots
It is a part of a scene, depicting one moment in the video which consists of:
1. An image to be shown in the video.
2. A dialogue in the video, spoken during the image being shown.
3. An image generation prompt, used to create the image described above.

# User Flows
## All Assets Generation
1. User Provides simple idea and clicks on generate script.
2. A list of boxes is created.
3. The Script (Text) is generated and shown in one separate box.
4. The Scenes (Text) are also generated and shown in each box.
5. In each scene box, the scene text is written.
6. Within each scene, multiple shots are generated.
7. For each shot, a text prompt is generated and from that text prompt an image is generated.


  