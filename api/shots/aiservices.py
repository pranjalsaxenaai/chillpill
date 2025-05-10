from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from api.settings import OPENAI_API_KEY
from utils.prompt_utils import PromptTemplates
import re



def generate_shots_ai(sceneContent):
    model = ChatOpenAI(api_key=OPENAI_API_KEY)
    
    sceneShotsChain = (
        ChatPromptTemplate.from_template(PromptTemplates.ShotsPromptWOScript)
        | model
        | StrOutputParser()
    )

    sceneShotsRunOutput = sceneShotsChain.invoke({"scene": sceneContent})
    print("Shots Generated Successfully")

    sceneShotsList = sceneShotsRunOutput.split('##Prompt')[1:]
    sceneShotsList = [re.sub(r"^\s*\d+:\s*", "", s) for s in sceneShotsList]

    # Print the generated prompts
    for prompt in sceneShotsList:
        print(f"##Prompt\n{prompt}")

    return sceneShotsList