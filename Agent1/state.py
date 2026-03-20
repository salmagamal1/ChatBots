from typing import TypedDict, Annotated, List, Union
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict, total=False):
    messages: Annotated[List[BaseMessage], operator.add]
    question: str
    intent: str
    sql_query: str
    sql_result: Union[List[dict], str]
    error: str
    revision_count: int