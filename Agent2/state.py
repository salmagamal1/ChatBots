from dataclasses import dataclass
from typing import Optional, List, Union

@dataclass
class State:
    input: Optional[str] = None                      
    intent: Optional[str] = None          
    cypher_query: Optional[str] = None    
    db_result: Optional[Union[List[dict], str]] = None 
    error: Optional[str] = None