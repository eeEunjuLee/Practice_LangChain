import json
from typing import Dict, List

from agent.a_chain import run_a_chain
from agent.b_chain import (
    run_b_chain_v1,
    run_b_chain_v2,
)
from agent.c_chain import run_c_chain

from utils.task_parser import parse_task_dsl
from utils.context_packing import build_execution_context

from tools.ffmpeg_executor import (
    run_ffmpeg_command,
    resolve_paths,
)

# -----------------------------------------------------------
# Agent Runner
# -----------------------------------------------------------
class FFmpegToyAgent:
    """
    Research-oriented Agent Runner.
    """

    def __init__(self):
        self.env = {
            "input_video_dir": r"C:\Users\ei994\PycharmProjects\FFmpeg_ToyAgent\aa_original_assets\video",
            "output_dir": r"C:\Users\ei994\PycharmProjects\FFmpeg_ToyAgent\bb_outputs",
        }

    def run(self, user_goal: str):
        """
        Run the full agent pipeline, including FFmpeg execution.

        Returns:
            {
              "tasks": [...],
              "execution_logs": [...]
            }
        """

        execution_logs: List[Dict] = []

        # ----------------------------------------------------
        # Step 1. a_chain: Goal → Planning → Task DSL
        # ----------------------------------------------------
        print("\n==============================")
        print("[Agent] Running a_chain")
        print("==============================")

        a_result = run_a_chain(user_goal)
        task_dsl_text = a_result["task_dsl"]

        print("\n[Task DSL]")
        print(task_dsl_text)

        # ----------------------------------------------------
        # Step 2. task_parser: TASK DSL → List[str]
        # ----------------------------------------------------
        tasks = parse_task_dsl(task_dsl_text)

        print("\n[Parsed Tasks]")
        for i, t in enumerate(tasks, 1):
            print(f"{i}. {t}")

        # ----------------------------------------------------
        # Step 3. Per-task execution
        # ----------------------------------------------------
        for idx, task in enumerate(tasks, 1):

            print("\n---------------------------------------------")
            print(f"[Agent] Processing task {idx}/{len(tasks)}")
            print(f"[Task] {task}")
            print("---------------------------------------------")

            # ---- b_chain v1 ----
            v1_output = run_b_chain_v1(task)

            print("\n[b_chain_v1 Output]")
            print(v1_output)

            # Skip non-executable tasks
            if "FFmpeg-capable: YES" not in v1_output:
                execution_logs.append({
                    "task_index": idx,
                    "task": task,
                    "ffmpeg_capable": False,
                    "b_chain_v1": v1_output,
                })
                continue

            # ---- b_chain v2 ----
            v2_output = run_b_chain_v2(task)

            print("\n[b_chain_v2 Output]")
            print(v2_output)

            # ---- context packing ----
            execution_context = build_execution_context(
                task_index=idx,
                task_text=task,
                b_chain_v1_output=v1_output,
                b_chain_v2_output=v2_output,
            )

            print("\n[Execution Context]")
            print(execution_context)

            # ---- c_chain ----
            ffmpeg_command = run_c_chain(execution_context)

            print("\n[c_chain Output - FFmpeg Command]")
            print(ffmpeg_command)

            # ---- resolve paths ----
            resolved_command = resolve_paths(ffmpeg_command, self.env)

            print("\n[Resolved FFmpeg Command]")
            print(resolved_command)

            # ---- FFmpeg execution ----
            print("\n[FFmpeg Execution]")
            exec_result = run_ffmpeg_command(resolved_command)

            print("\n[FFmpeg Result]")
            for k, v in exec_result.items():
                print(f"{k}:")
                print(v)
                print("-" * 40)

            # ---- logging ----
            execution_logs.append({
                "task_index": idx,
                "task": task,
                "ffmpeg_capable": True,
                "b_chain_v1": v1_output,
                "b_chain_v2": v2_output,
                "execution_context": execution_context,
                "ffmpeg_command": ffmpeg_command,
                "ffmpeg_result": exec_result,
            })

        return {
            "tasks": tasks,
            "execution_logs": execution_logs,
        }


# -----------------------------------------------------------
# Execution
# -----------------------------------------------------------
if __name__ == "__main__":

    user_goal = """
    mv_complicated.mp4: 01:10 ~ 01:37
    mv_sk8er_boi.mp4: 00:46 ~ 01:03
    mv_my_happy_ending.mp4: 00:51 ~ 01:21
    mv_girlfriend.mp4: 00:12 ~ 00:36
    mv_what_the_hell.mp4: 00:50 ~ 01:16
    mv_rock_n_roll.mp4: 01:21 ~ 01:53
    이 구간들로 유튜브 쇼츠 만들어줘
    """

    agent = FFmpegToyAgent()
    agent.run(user_goal)