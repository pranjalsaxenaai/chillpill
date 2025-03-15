from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from api.settings import OPENAI_API_KEY
import re


def generate_scenes(scriptContent):
    model = ChatOpenAI(api_key=OPENAI_API_KEY)
    scenesPromptTemplate = """
    Below is a movie script, please generate various scenes for this script. 
    Each scene should start with heading ##Scene.\n\n {script}
    """
    scenesChain = (
        ChatPromptTemplate.from_template(scenesPromptTemplate)
        | model
        | StrOutputParser()
    )

    scenesRunOutput = scenesChain.invoke({"script": scriptContent})
    print("Scenes Generated Successfully")

    scenesList = scenesRunOutput.split('##Scene')[1:]
    scenesList = [re.sub(r"^\s*\d+:\s*", "", s) for s in scenesList]

    # Print the generated scenes
    for scene in scenesList:
        print(f"##Scene\n{scene}")

    return scenesList