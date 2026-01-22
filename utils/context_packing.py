from typing import Any, Dict, Optional


def build_execution_context(
        task_index: int,
        task_text: str,
        b_chain_v1_output: str,
        b_chain_v2_output: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Build an execution context by packing outputs from b_chain
    without performing any semantic interpretation or normalization.

    This context is intended to be consumed by c_chain as-is.

    Args:
        task_index (int):
            Index of the task in the overall task list (for traceability).

        task_text (str):
            Original task text from a_chain.

        b_chain_v1_output (str):
            Natural-language interpretation from b_chain_v1
            (FFmpeg-capable decision, operation type, required info).

        b_chain_v2_output (Optional[str]):
            Structured representation from b_chain_v2, if available.
            May be None for non-FFmpeg-capable tasks.

    Returns:
        Dict[str, Any]: Execution context dictionary.
    """

    context: Dict[str, Any] = {
        "task_index": task_index,
        "task_text": task_text,
        "analysis": {
            "b_chain_v1": b_chain_v1_output,
            "b_chain_v2": b_chain_v2_output,
        },
    }

    return context


# ------------------------------------------------------------
# Execution
# ------------------------------------------------------------
if __name__ == "__main__":

    example_context = build_execution_context(
        task_index=14,
        task_text="Adjust audio levels across all segments to ensure consistency.",
        b_chain_v1_output="""
                            FFmpeg-capable: YES
                            Operation type: Audio normalization
                            Required information: The specific video file(s) to process and the desired audio level settings.
                                """,
        b_chain_v2_output="""
                            {
                              "task": "Adjust Audio Levels",
                              "description": "Ensure consistency of audio levels across all segments of the video.",
                              "parameters": {
                                "operation": "normalize",
                                "target": "consistent audio levels",
                                "segments": "all"
                              }
                            }
                                """,
    )

    from pprint import pprint
    pprint(example_context)