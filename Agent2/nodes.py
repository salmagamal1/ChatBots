import os
from llama_index.llms.groq import Groq
from llama_index.llms.google_genai import GoogleGenAI
from Agent2.prompts import (
    GRAPH_CONCEPT_EXPLANATION, INTENT_CLASSIFIER_PROMPT, 
    GENERAL_PROMPT, OUT_OF_CONTEXT_PROMPT, ADD_CYPHER_PROMPT, 
    INQUIRE_CYPHER_PROMPT, SYNTHESIS_PROMPT, UPDATE_CYPHER_PROMPT, 
    DELETE_CYPHER_PROMPT
)
from Agent2.state import State

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from setup_neo4j import execute_query

llm = Groq(model="openai/gpt-oss-120b", temperature=0.0, api_key=os.getenv("GROQ_API_KEY"),max_tokens=4096)
# llm = GoogleGenAI(model="gemini-2.5-flash", temperature=0.0, api_key=os.getenv("GEMINI"))


# first node - intent classifier 
def classify_intent(state: State) -> State:
    prompt = INTENT_CLASSIFIER_PROMPT.format(user_input=state["question"])  
    response = llm.complete(prompt)
    valid_intents = ["general", "out_of_context", "add", "inquire", "update", "delete"]
    
    if response.text.strip().lower() in valid_intents:
        state["intent"] = response.text.strip().lower()
    else:
        state["intent"] = "out_of_context"  
        
    print(f"[DEBUG] 0. CLASSIFIED INTENT: {state['intent']}")
    return state

def handle_general(state: State) -> State:
    print("[DEBUG] Handling general intent.")
    prompt = GENERAL_PROMPT.format(user_input=state["question"])
    response = llm.complete(prompt)
    state["final_response"] = response.text.strip()
    return state

def handle_out_of_context(state: State) -> State:
    print("[DEBUG] Handling out_of_context intent.")
    prompt = OUT_OF_CONTEXT_PROMPT.format(user_input=state["question"])
    response = llm.complete(prompt)
    state["final_response"] = response.text.strip()
    return state

def generate_add_cypher(state: State) -> State:
    print("[DEBUG] Generating add Cypher query.")
    prompt = ADD_CYPHER_PROMPT.format(
        graph_explanation=GRAPH_CONCEPT_EXPLANATION,
        user_input=state["question"]
    )
    response = llm.complete(prompt)
    state["cypher_query"] = response.text.strip()
    return state

def generate_inquire_cypher(state: State) -> State:
    print("[DEBUG] Generating inquire Cypher query.")
    prompt = INQUIRE_CYPHER_PROMPT.format(
        graph_explanation=GRAPH_CONCEPT_EXPLANATION,
        user_input=state["question"] 
    )  
    response = llm.complete(prompt)
    state["cypher_query"] = response.text.strip()
    return state

def generate_update_cypher(state: State) -> State:
    print("[DEBUG] Generating update Cypher query.")
    prompt = UPDATE_CYPHER_PROMPT.format(
        graph_explanation=GRAPH_CONCEPT_EXPLANATION,
        user_input=state["question"] 
    )
    response = llm.complete(prompt)
    state["cypher_query"] = response.text.strip()
    return state

def generate_delete_cypher(state: State) -> State:
    print("[DEBUG] Generating delete Cypher query.")
    prompt = DELETE_CYPHER_PROMPT.format(
        graph_explanation=GRAPH_CONCEPT_EXPLANATION,
        user_input=state["question"]
    )
    response = llm.complete(prompt)
    state["cypher_query"] = response.text.strip()
    return state

def execute_cypher(state: State) -> State:
    print(f"[DEBUG] Executing Cypher query: {state['cypher_query']}")
    if not state["cypher_query"]:
        state["error"] = "No Cypher query to execute."
        return state
        
    try:
        results = execute_query(state["cypher_query"])
        state["db_result"] = results

        if isinstance(results, list):
            print(f"[DEBUG] Database returned {len(results)} result(s).")
        else:
            print(f"[DEBUG] Database returned: {results}")
    except Exception as e:
        print(f"[DEBUG] Database Error: {e}")
        state["error"] = str(e)
        
    return state


def synthesize_response(state: State) -> State:
    print("[DEBUG] Synthesizing final response.")
    
    # handle db errors
    if state["error"]:
        state["final_response"] = f"An error occurred while accessing the database: {state['error']}"
        return state
        
    if state["intent"] in ["general", "out_of_context"]:
        return state
    
    db_result_str = str(state["db_result"]) if state["db_result"] else "No results found."
    prompt = SYNTHESIS_PROMPT.format(
        user_input=state["question"],
        intent=state["intent"],
        db_result=db_result_str
    )
    response = llm.complete(prompt)
    state["final_response"] = response.text.strip()
    print(f"[DEBUG] Final synthesized response: {state['final_response']}")
    return state