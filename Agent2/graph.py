from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent, Event
from .state import State
from .nodes import (
    classify_intent, handle_general, handle_out_of_context,
    generate_add_cypher, generate_inquire_cypher,
    generate_update_cypher, generate_delete_cypher,
    execute_cypher, synthesize_response
)

# --- Define the Events ---
class ClassifiedEvent(Event):
    state: State

class CypherEvent(Event):
    state: State

class DbResultEvent(Event):
    state: State


# --- Define the Workflow ---
class KnowledgeGraphAgent(Workflow):
    
    @step
    async def classify(self, ev: StartEvent) -> ClassifiedEvent:
        history = getattr(ev, "chat_history", [])

        current_state: State = {
            "question": ev.user_input,
            "chat_history": history,
            "intent": None,
            "cypher_query": None,
            "db_result": None,
            "final_response": None,
            "error": None
        }
        
        # Run the classifier node 
        updated_state = classify_intent(current_state)
        return ClassifiedEvent(state=updated_state)

    @step
    async def route_and_generate(self, ev: ClassifiedEvent) -> CypherEvent | StopEvent:
        """The Router Step that directs traffic based on the intent."""
        state = ev.state
        intent = state["intent"]
        
        # --- Conversational Intents ---
        if intent == "general":
            state = handle_general(state)
            return StopEvent(result=state["final_response"])
            
        elif intent == "out_of_context":
            state = handle_out_of_context(state)
            return StopEvent(result=state["final_response"])
            
        # --- Database Intents ---
        elif intent == "add":
            state = generate_add_cypher(state)
            return CypherEvent(state=state)
            
        elif intent == "inquire":
            state = generate_inquire_cypher(state)
            return CypherEvent(state=state)
            
        elif intent == "update":
            state = generate_update_cypher(state)
            return CypherEvent(state=state)
            
        elif intent == "delete":
            state = generate_delete_cypher(state)
            return CypherEvent(state=state)
            
        else:
            state = handle_out_of_context(state)
            return StopEvent(result=state["final_response"])

    @step
    async def execute_database(self, ev: CypherEvent) -> DbResultEvent:
        updated_state = execute_cypher(ev.state)
        return DbResultEvent(state=updated_state)

    @step
    async def synthesize(self, ev: DbResultEvent) -> StopEvent:
        final_state = synthesize_response(ev.state)
        return StopEvent(result=final_state["final_response"])