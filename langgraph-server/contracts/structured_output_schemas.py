from pydantic import BaseModel, Field
from typing import List

class SceneOutput(BaseModel):
    scene_number: int = Field(description="The sequence number of the scene")
    scene_description: str = Field(description="A description of the scene")

class ScenesOutput(BaseModel):
    scenes: List[SceneOutput] = Field(description="A list of scenes in the output")

class ImageOutput(BaseModel):
    image_number: int = Field(description="The sequence number of the image")
    image_prompt: str = Field(description="The image generation prompt for the image")

class ImagesOutput(BaseModel):
    images: List[ImageOutput] = Field(description="A list of images in the output")