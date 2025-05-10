class PromptTemplates:
    """
    This class contains the prompt templates for various tasks.
    """
    ScriptPromptTemplate = """
    You are a creative script writer. 
    Write a descriptive script for a short film on below idea:\n\n{idea}
    """
    ScriptTitlePromptTemplate = "Create a 3-5 words title on below idea:\n\n{idea}"

    ScenesPromptTemplate = """
    Below is a movie script, please generate various scenes for this script. 
    Each scene should start with heading ##Scene.\n\n {script}
    """

    ShotsPromptWOScript = """
    Below is a Scene Description. 
    Looking at the Scene Description, 
    think of 3-4 shots and create image generation prompts for these shots.
    Only provide the image generation prompts without frame description. 
    Each prompt should start with heading ##Prompt. \n\n {scene}\n\n 
    """
