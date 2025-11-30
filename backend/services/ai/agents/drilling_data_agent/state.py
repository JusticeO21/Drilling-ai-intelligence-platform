from langgraph.graph import MessagesState
from typing import Literal, Any


class DrillAgentState(MessagesState):
    user_id: str
    dataset_id: str
    metadata_dict: dict
    metadata: str
    query_type: Literal["simple", "complex"]
    python_code: str
    execution_result: Any
    error: str
    final_response: str
