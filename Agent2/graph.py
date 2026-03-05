from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent, Event
from Agent2.state import State
from Agent2.nodes import classify_intent, generate_cypher,execute_cypher, synthesize_response

# 1. Define the intermediate Events
class ClassifiedEvent(Event):
    state: State

class CypherEvent(Event):
    state: State

class DbResultEvent(Event):
    state: State

# 2. Build the Orchestrator
class KnowledgeGraphAgent(Workflow):
    
    @step
    async def classify(self, ev: StartEvent) -> ClassifiedEvent:
        current_state = State(input=ev.user_input)
        updated_state =await classify_intent(current_state)
        return ClassifiedEvent(state=updated_state)

    @step
    async def generate_cypher(self, ev: ClassifiedEvent) -> CypherEvent:
        updated_state = await generate_cypher(ev.state)
        return CypherEvent(state=updated_state)

    @step
    async def execute_database(self, ev: CypherEvent) -> DbResultEvent:
        updated_state = await execute_cypher(ev.state)
        return DbResultEvent(state=updated_state)

    @step
    async def synthesize(self, ev: DbResultEvent) -> StopEvent:
        final_state = await synthesize_response(ev.state)
        return StopEvent(result=final_state.db_result)