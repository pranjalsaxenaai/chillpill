from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from api.settings import OPENAI_API_KEY

def generate_shots(sceneContent):
    model = ChatOpenAI(api_key=OPENAI_API_KEY)
    shotsPromptWOScript = """
    Below is a Scene Description. 
    Looking at the Scene Description, 
    think of 3-4 shots and create image generation prompts for these shots.
    Only provide the image prompts without frame description. \n\n {scene}\n\n 
    """
    sceneShotsChain = (
        ChatPromptTemplate.from_template(shotsPromptWOScript)
        | model
        | StrOutputParser()
    )

    shotsPromptResult = sceneShotsChain.batch(
        [{"scene":value} for value in scenesList])