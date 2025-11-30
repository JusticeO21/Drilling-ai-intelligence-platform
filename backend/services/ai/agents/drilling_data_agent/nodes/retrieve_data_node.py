from services.ai.agents.drilling_data_agent.state import DrillAgentState
from services.ai.agents.drilling_data_agent.tools import extract_metadata
from services.ai.agents.drilling_data_agent.tools import format_metadata_for_llm
from common.logging import logger


def retrieve_metadata_node(state: DrillAgentState) -> DrillAgentState:
    """Extract and format metadata for query processing"""
    logger.info(
        f"[NODE] Starting retrieve_metadata_node for user {state.get('user_id')}, dataset {state.get('dataset_id')}"
    )

    query = state.get("messages")[-1].content
    metadata = extract_metadata(
        user_id=state.get("user_id"), dataset_id=state.get("dataset_id"), query=query
    )

    state["metadata"] = format_metadata_for_llm(metadata)
    state["metadata_dict"] = metadata

    logger.info(
        f"[NODE] Completed retrieve_metadata_node - extracted {len(metadata.get('columns', []))} columns"
    )
    return state
