import os
from llama_index.llms.groq import Groq
from llama_index.llms.google_genai import GoogleGenAI
from Agent2 import state
from Agent2.prompts import INTENT_CLASSIFIER_PROMPT,CYPHER_GENERATION_PROMPT,SYNTHESIS_PROMPT
from Agent2.state import State

import sys
# Ensure Python can find the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from setup_neo4j import execute_query


llm = Groq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"))
# llm = Groq(
#     model="llama3-8b-8192",
#     api_key=os.getenv("GROQ_API_KEY"),
#     base_url="https://api.groq.com/openai/v1"
# )

# llm = GoogleGenAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
# llm = GoogleGenAI(model="gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))


# firat node - intent classifier 
# we change to async function for gemini
async def classify_intent(state: State) -> State:
    prompt = INTENT_CLASSIFIER_PROMPT.format(user_input=state.input)  
    response = await llm.acomplete(prompt)
    state.intent = response.text.strip().lower()
    return state


# second node - cypher query generator
async def generate_cypher(state: State) -> State:
    if state.intent == "general":
         return state
    prompt = CYPHER_GENERATION_PROMPT.format(intent=state.intent, user_input=state.input)
    response = await llm.acomplete(prompt)
    state.cypher_query = response.text.strip()
    return state


# thrid node - execute cypher query and store result
async def execute_cypher(state: State) -> State:
    if state.intent in ["general", None] or not state.cypher_query:
        return state

    print("\n" + "="*40)
    print(f"[DEBUG] 1. INTENT: {state.intent}")
    print(f"[DEBUG] 2. CYPHER:{state.cypher_query}")
    try:
        results = await execute_query(state.cypher_query)
        state.db_result = results
    except Exception as e:
        state.error = str(e)
        
    return state


# last node -> synthesize final response  (human-readable response)
# edit -> fix issue gemini not response about "add" correctly
async def synthesize_response(state: State) -> State:
    # if state.error:
    #     db_info = f"Database Error: {state.error}"
    # elif state.db_result == []:
    #     # If the result is an empty list, it means the write/delete was successful!
    #     db_info = "Operation successful. The graph was updated, but no records were returned."
    # elif state.db_result:
    #     db_info = state.db_result
    # else:
    #     db_info = "No database data needed."
    if state.error:
        db_info = f"Database Error: {state.error}"
    elif state.intent in ["add", "edit", "delete"] and state.db_result == []:
        # If it's a write operation and returns an empty list, it's a massive success.
        db_info = "SYSTEM MESSAGE: SUCCESS! The database was successfully updated. Tell the user it was added."
    elif state.db_result:
        db_info = str(state.db_result)
    else:
        db_info = "No database data was found."
    prompt = SYNTHESIS_PROMPT.format(
        user_input=state.input,
        db_result=state.db_result if state.db_result else "No database interaction"
    )
    response = await llm.acomplete(prompt)
    state.db_result = str(response.text).strip()
    return state
    
