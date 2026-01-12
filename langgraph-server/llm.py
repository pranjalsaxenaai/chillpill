from pydantic import BaseModel, Field
import os, getpass
from langchain_openai import ChatOpenAI
import dotenv

dotenv.load_dotenv()

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("OPENAI_API_KEY")
_set_env("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "KahaaniAI"

llm = ChatOpenAI(model="gpt-4o")

def llm_text(prompt: str) -> str:
    """
    Placeholder: wire this to your model (OpenAI, Azure OpenAI, etc.)
    Return plain text.
    """
    return llm.invoke(prompt).content

def llm_structured(prompt: str, schema: type[BaseModel]) -> BaseModel:
    """
    Placeholder: wire this to a structured-output call.
    """

    structured_llm = llm.with_structured_output(schema)
    return structured_llm.invoke(prompt)