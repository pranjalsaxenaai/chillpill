from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from api.settings import OPENAI_API_KEY
from projects.services import get_project

def generate_script(project_id, project_idea):

    # Fetch API Key from settings
    openai_api_key = OPENAI_API_KEY
    model = ChatOpenAI(api_key=openai_api_key)
    scriptPromptTemplate = "You are a creative script writer. Write a descriptive script for a short film on below idea:\n\n{idea}"
    scriptTitlePromptTemplate = "Create a 3-5 words title on below idea:\n\n{idea}"

    scriptChain = (
        ChatPromptTemplate.from_template(scriptPromptTemplate)
        | model
        | StrOutputParser()
    )

    titleChain = (
        ChatPromptTemplate.from_template(scriptTitlePromptTemplate)
        | model
        | StrOutputParser()
    )

    runnable = RunnableParallel(Title=titleChain, Script=scriptChain)

    project = get_project(project_id)
    # If no project idea is provided, fetch the project idea from the project description
    if project_idea is None:
        project_idea = project["project_desc"]
    
    runOutput = runnable.invoke({"idea": project_idea})
    print("Script Generated Successfully")

    return runOutput, project

