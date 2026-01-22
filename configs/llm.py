import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI


def get_llm():
    """
    Central LLM factory.
    This is the ONLY place where the model is selected.
    """

    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY"),
    )