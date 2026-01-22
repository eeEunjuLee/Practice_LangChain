from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from configs.llm import get_llm
from prompts.c_chain_prompts import C_CHAIN_EXECUTION_PROMPT

# ------------------------------------------------------------
# c_chain: Execution Context → FFmpeg command
# ------------------------------------------------------------
def build_c_chain():
    """
    c_chain:
    execution context
      → LLM
      → FFmpeg command (string)
    """

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", C_CHAIN_EXECUTION_PROMPT),
            ("human", "{execution_context}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()
    return chain


# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------
def run_c_chain(execution_context: Dict[str, Any]) -> str:
    """
    Generate an FFmpeg command from an execution context.

    Args:
        execution_context (dict):
            Packed context containing task text and b_chain outputs.

    Returns:
        str: FFmpeg command
    """

    chain = build_c_chain()

    # context를 문자열로 그대로 전달
    return chain.invoke(
        {"execution_context": execution_context}
    )


# ------------------------------------------------------------
# Execution
# ------------------------------------------------------------
if __name__ == "__main__":

    example_context = {
        "task_index": 6,
        "task_text": "Extract the highlight segment from mv_complicated.mp4 from 01:10 to 01:37.",
        "analysis": {
                        "b_chain_v1":"""
                                        FFmpeg-capable: YES
                                        Operation type: Video trimming
                                        Required information: input file, start time, end time
                                            """,
                        "b_chain_v2":"""
                                        {
                                          "task": "extract_segment",
                                          "input_file": "mv_complicated.mp4",
                                          "start_time": "01:10",
                                          "end_time": "01:37"
                                        }
                                            """
                    }
                }

    cmd = run_c_chain(example_context)

    print("\n===== GENERATED FFmpeg COMMAND =====")
    print(cmd)
