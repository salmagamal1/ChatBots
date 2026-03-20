import sqlite3
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from .state import AgentState
from .prompts import (INTENT_PROMPT,SYSTEM_PROMPT,REPLAN_PROMPT,RESPONSE_PROMPT,get_schema_string)

load_dotenv()

llm = ChatGroq( model="openai/gpt-oss-120b", temperature=0.0, api_key=os.getenv("GROQ_API_KEY"))

DB_PATH = "inventory_chatbot.db"


# ---------------- INTENT CLASSIFIER ---------------- #

def intent_classifier_node(state: AgentState):

    prompt = INTENT_PROMPT.format(question=state["question"])

    res = llm.invoke([
        HumanMessage(content=prompt)
    ])

    intent = res.content.strip().upper()

    if intent not in ["CHITCHAT", "DATABASE_QUERY"]:
        intent = "CHITCHAT"

    return {"intent": intent}


# ---------------- CHITCHAT NODE ---------------- #

def chitchat_node(state: AgentState):

    res = llm.invoke([
        HumanMessage(content=state["question"])
    ])

    return {
        "messages": [AIMessage(content=res.content)]
    }


# ---------------- SQL GENERATOR ---------------- #

def sql_generator_node(state: AgentState):

    schema = get_schema_string(DB_PATH)

    sys_msg = SystemMessage(
        content=SYSTEM_PROMPT.format(schema=schema)
    )

    res = llm.invoke([
        sys_msg,
        HumanMessage(content=state["question"])
    ])

    query = res.content.replace("```sql", "").replace("```", "").strip()

    return {
        "sql_query": query,
        "revision_count": 0,
        "error": None
    }


# ---------------- SQL EXECUTOR ---------------- #

def sql_executor_node(state: AgentState):

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(state["sql_query"])
        rows = cursor.fetchall()

        result = [dict(row) for row in rows]

        conn.close()

        return {
            "sql_result": result,
            "error": None
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ---------------- SQL CORRECTOR ---------------- #

def sql_corrector_node(state: AgentState):

    prompt = REPLAN_PROMPT.format(
        error=state["error"],
        query=state["sql_query"]
    )

    res = llm.invoke([
        HumanMessage(content=prompt)
    ])

    query = res.content.replace("```sql", "").replace("```", "").strip()

    return {
        "sql_query": query,
        "revision_count": state["revision_count"] + 1
    }


# ---------------- FINAL RESPONSE ---------------- #

def responder_node(state: AgentState):

    prompt = RESPONSE_PROMPT.format(
        question=state["question"],
        result=state["sql_result"],
        sql=state["sql_query"]
    )

    res = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return {
        "messages": [AIMessage(content=res.content)]
    }