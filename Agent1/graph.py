from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .state import AgentState
from .nodes import (intent_classifier_node,chitchat_node,sql_generator_node,sql_executor_node,sql_corrector_node,responder_node)


# ---------------- INTENT ROUTER ---------------- #

def route_intent(state: AgentState):

    if state["intent"] == "DATABASE_QUERY":
        return "generator"

    return "chitchat"


# ---------------- SQL ERROR LOOP ---------------- #

def should_continue(state: AgentState):

    if state.get("error") and state.get("revision_count", 0) < 3:
        return "corrector"

    return "responder"


# ---------------- GRAPH ---------------- #

workflow = StateGraph(AgentState)

workflow.add_node("intent_classifier", intent_classifier_node)
workflow.add_node("chitchat", chitchat_node)

workflow.add_node("generator", sql_generator_node)
workflow.add_node("executor", sql_executor_node)
workflow.add_node("corrector", sql_corrector_node)
workflow.add_node("responder", responder_node)

workflow.set_entry_point("intent_classifier")

workflow.add_conditional_edges(
    "intent_classifier",
    route_intent,
    {
        "generator": "generator",
        "chitchat": "chitchat"
    }
)

workflow.add_edge("generator", "executor")

workflow.add_conditional_edges(
    "executor",
    should_continue,
    {
        "corrector": "corrector",
        "responder": "responder"
    }
)

workflow.add_edge("corrector", "executor")
workflow.add_edge("responder", END)
workflow.add_edge("chitchat", END)


memory = MemorySaver()

app = workflow.compile(checkpointer=memory)