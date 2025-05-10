from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from api.settings import OPENAI_API_KEY
from utils.prompt_utils import PromptTemplates

def generate_script_ai(project_idea):

    # Fetch API Key from settings
    model = ChatOpenAI(api_key=OPENAI_API_KEY)

    scriptChain = (
        ChatPromptTemplate.from_template(PromptTemplates.ScriptPromptTemplate)
        | model
        | StrOutputParser()
    )

    titleChain = (
        ChatPromptTemplate.from_template(PromptTemplates.ScriptTitlePromptTemplate)
        | model
        | StrOutputParser()
    )

    runnable = RunnableParallel(Title=titleChain, Script=scriptChain)
    runOutput = runnable.invoke({"idea": project_idea})
    print("Script Generated Successfully")

    return runOutput

