from typing import Dict, List

from agent.a_chain import run_a_chain
from agent.b_chain import (
    run_b_chain_v1,
    run_b_chain_v2,
)
from agent.c_chain import run_c_chain
from utils.task_parser import parse_task_dsl
from utils.context_packing import build_execution_context


# -----------------------------------------------------------
# Agent Runner
# -----------------------------------------------------------
class FFmpegToyAgent:
    """
    Agent Runner:
    - Orchestrates a_chain → task_parser → b_chain_v1 → b_chain_v2
    - Does NOT execute FFmpeg
    - Does NOT define DSL
    """

    def __init__(self):
        pass

    def run(self, user_goal: str) -> Dict[str, List[str]]:
        """
        Run the agent pipeline end-to-end (observation only).

        Returns:
            {
              "tasks": [...],
              "b_chain_v1_outputs": [...],
              "b_chain_v2_outputs": [...]
            }
        """

        # ----------------------------------------------------
        # Step 1. a_chain: Goal → Planning → Task DSL
        # ----------------------------------------------------
        a_result = run_a_chain(user_goal)
        task_dsl_text = a_result["task_dsl"]

        # ----------------------------------------------------
        # Step 2. task_parser: TASK DSL → List[str]
        # ----------------------------------------------------
        tasks = parse_task_dsl(task_dsl_text)

        b_chain_v1_outputs = []
        b_chain_v2_outputs = []

        # ----------------------------------------------------
        # Step 3. b_chain_v1 / v2
        # ----------------------------------------------------
        for idx, task in enumerate(tasks, 1):
            print(f"\n[Agent] Processing task {idx}/{len(tasks)}")
            print(f"[Task] {task}")

            # ---- b_chain v1: capability 판단 ----
            v1_output = run_b_chain_v1(task)

            print("\n[b_chain_v1 Output]")
            print(v1_output)

            b_chain_v1_outputs.append(v1_output)

            # ---- b_chain v2: 구조화 시도 (조건부) ----
            if "FFmpeg-capable: YES" in v1_output:
                v2_output = run_b_chain_v2(task)

                print("\n[b_chain_v2 Output]")
                print(v2_output)

                # ----------------------------------------------------
                # execution context packing
                # ----------------------------------------------------
                execution_context = build_execution_context(
                    task_index=idx,
                    task_text=task,
                    b_chain_v1_output=v1_output,
                    b_chain_v2_output=v2_output,
                )

                print("\n[Execution Context]")
                print(execution_context)

                # ----------------------------------------------------
                # c_chain (FFmpeg command generation)
                # ----------------------------------------------------
                ffmpeg_command = run_c_chain(execution_context)

                print("\n[c_chain Output - FFmpeg Command]")
                print(ffmpeg_command)

                b_chain_v2_outputs.append(v2_output)

        return {
            "tasks": tasks,
            "b_chain_v1_outputs": b_chain_v1_outputs,
            "b_chain_v2_outputs": b_chain_v2_outputs,
        }


# -----------------------------------------------------------
# Execution
# -----------------------------------------------------------
if __name__ == "__main__":

    user_goal = """
    mv_complicated.mp4: 01:10 ~ 01:37
    mv_sk8er_boi.mp4:00:46 ~ 01:03
    mv_my_happy_ending.mp4: 00:51 ~ 01:21
    mv_girlfriend.mp4: 00:12 ~ 00:36
    mv_what_the_hell.mp4: 00:50 ~ 01:16
    mv_rock_n_roll.mp4: 01:21 ~ 01:53
    이 구간들로 유튜브 쇼츠 만들어줘
    """

    agent = FFmpegToyAgent()
    agent.run(user_goal)