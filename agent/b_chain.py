from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from configs.llm import get_llm
from prompts.b_chain_prompts import (
    B_CHAIN_TASK_INTERPRET_PROMPT,
    B_CHAIN_STRUCTURED_PROMPT,
)

# ------------------------------------------------------------
# b_chain v1: Task → FFmpeg-oriented interpretation
# ------------------------------------------------------------
def build_b_chain_v1():
    """
    b_chain v1:
    human-oriented task
      → LLM
      → FFmpeg-oriented task interpretation
    """

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", B_CHAIN_TASK_INTERPRET_PROMPT),
            ("human", "{task}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()
    return chain


def run_b_chain_v1(task: str) -> str:
    """
    Interpret a single task and return FFmpeg-oriented meaning.
    """
    chain = build_b_chain_v1()
    return chain.invoke({"task": task})


# ------------------------------------------------------------
# b_chain v2: Task → LLM-generated structured representation
# ------------------------------------------------------------
def build_b_chain_v2():
    """
    b_chain v2:
    human-oriented task
      → LLM
      → LLM-generated structured representation (DSL-free)
    """

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", B_CHAIN_STRUCTURED_PROMPT),
            ("human", "{task}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()
    return chain


def run_b_chain_v2(task: str) -> str:
    """
    Generate a structured representation for a single FFmpeg-capable task.

    NOTE:
    - No schema is enforced
    - Output is used only for observation
    """
    chain = build_b_chain_v2()
    return chain.invoke({"task": task})


# ------------------------------------------------------------
# Execution
# ------------------------------------------------------------
if __name__ == "__main__":

    test_tasks = [
        "Extract the highlight segment from mv_complicated.mp4 from 01:10 to 01:37.",
        "Adjust the audio levels of all clips to ensure consistency.",
        "Upload the completed video to YouTube.",
    ]

    for t in test_tasks:
        print("\n===== TASK =====")
        print(t)

        print("\n--- b_chain_v1 OUTPUT ---")
        v1_out = run_b_chain_v1(t)
        print(v1_out)

        if "FFmpeg-capable: YES" in v1_out:
            print("\n--- b_chain_v2 OUTPUT ---")
            print(run_b_chain_v2(t))
