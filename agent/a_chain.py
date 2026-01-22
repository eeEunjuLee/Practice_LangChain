from typing import Any, Dict

from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from configs.llm import get_llm
from prompts.a_chain_prompts import (
    A_CHAIN_PLANNING_PROMPT,
    A_CHAIN_TASK_PROMPT,
)


# -----------------------------------------------------------
# a_chain1: Goal → Planning
# -----------------------------------------------------------
def build_a_chain1():
    """
    a_chain1:
    user goal
      → LLM
      → planning (natural language reasoning)
    """
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", A_CHAIN_PLANNING_PROMPT),
            ("human", "{user_goal}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()
    return chain


# -----------------------------------------------------------
# a_chain2: Planning → Task sequence (loose DSL)
# -----------------------------------------------------------
def build_a_chain2():
    """
    a_chain2:
    planning
      → LLM
      → task combination & order (loose DSL)
    """
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", A_CHAIN_TASK_PROMPT),
            ("human", "{planning}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()
    return chain


# -----------------------------------------------------------
# a_chain = a_chain1 | a_chain2
# -----------------------------------------------------------
def build_a_chain():
    """
    Full a_chain:
    user goal
      → planning
      → task DSL
    """

    a_chain1 = build_a_chain1()
    a_chain2 = build_a_chain2()

    # RunnableSequence allows explicit multi-step chaining
    a_chain = RunnableSequence(
        steps=[
            # step 1: planning
            a_chain1,
            # step 2: task DSL
            a_chain2,
        ]
    )

    return a_chain


# -----------------------------------------------------------
# Public API
# -----------------------------------------------------------
def run_a_chain(user_goal: str) -> Dict[str, Any]:
    """
    Execute a_chain and return both intermediate & final outputs.
    (중요: 중간 결과를 버리지 않는다)
    """

    a_chain1 = build_a_chain1()
    a_chain2 = build_a_chain2()

    planning = a_chain1.invoke({"user_goal": user_goal})
    task_dsl = a_chain2.invoke({"planning": planning})

    return {
        "user_goal": user_goal,
        "planning": planning,
        "task_dsl": task_dsl,
    }


# ------------------------------------------------------------
# Execution
# ------------------------------------------------------------
if __name__ == "__main__": # terminal session 22

    user_goal = """
    mv_complicated.mp4: 01:10 ~ 01:37
    mv_sk8er_boi.mp4:00:46 ~ 01:03
    mv_my_happy_ending.mp4: 00:51 ~ 01:21
    mv_girlfriend.mp4: 00:12 ~ 00:36
    mv_what_the_hell.mp4: 00:50 ~ 01:16
    mv_rock_n_roll.mp4: 01:21 ~ 01:53
    이 구간들로 유튜브 쇼츠 만들어줘
    """

    result = run_a_chain(user_goal)

    print("\n===== USER GOAL =====")
    print(result["user_goal"])

    print("\n===== PLANNING =====")
    print(result["planning"])

    print("\n===== TASK DSL =====")
    print(result["task_dsl"])
