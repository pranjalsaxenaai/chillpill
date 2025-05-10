from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from api.settings import OPENAI_API_KEY
import re
from utils.prompt_utils import PromptTemplates


def generate_scenes_ai(scriptContent):
    model = ChatOpenAI(api_key=OPENAI_API_KEY)
    
    scenesChain = (
        ChatPromptTemplate.from_template(PromptTemplates.ScenesPromptTemplate)
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