import re
from typing import List


def parse_task_dsl(task_dsl_text: str) -> List[str]:
    """
    Parse a TASK DSL string produced by a_chain into a list of task strings.

    Design principles:
    - Deterministic (no LLM)
    - Conservative (do not modify meaning)
    - Robust to multi-line tasks
    """

    lines = task_dsl_text.splitlines()

    tasks: List[str] = []
    current_task = ""

    for line in lines:
        line = line.strip()

        # skip empty lines
        if not line:
            continue

        # case 1: numbered task start (e.g., "1. ...")
        match = re.match(r"^(\d+)\.\s+(.*)", line)
        if match:
            # flush previous task
            if current_task:
                tasks.append(current_task.strip())
                current_task = ""

            # start new task without the numbering
            current_task = match.group(2).strip()

        # case 2: continuation of previous task (wrapped line)
        else:
            if current_task:
                current_task += " " + line
            else:
                # edge case: no numbering but text exists
                current_task = line

    # flush last task
    if current_task:
        tasks.append(current_task.strip())

    return tasks

# -----------------------------------------------------------
# Execution
# -----------------------------------------------------------
if __name__ == "__main__":

    sample_task_dsl = """
    1. Extract the highlight segment from mv_complicated.mp4 from 01:10 to 01:37.
    2. Extract the highlight segment from mv_sk8er_boi.mp4 from 00:46 to 01:03.
    3. Organize the extracted clips in a logical order for the final video.
    4. Ensure all clips are trimmed to the same aspect ratio and resolution.
    """

    parsed = parse_task_dsl(sample_task_dsl)

    print("===== PARSED TASKS =====")
    for i, t in enumerate(parsed, 1):
        print(f"{i}: {t}")