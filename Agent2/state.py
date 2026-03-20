from typing_extensions import TypedDict
from typing import Optional, List, Union, Dict, Any

class State(TypedDict):
    question: str
    chat_history: List[Dict[str, str]]
    intent: Optional[str]
    cypher_query: Optional[str]
    db_result: Optional[Union[List[Any], str]]
    final_response: Optional[str]
    error: Optional[str]