from services.ai.agents.drilling_data_agent.state import DrillAgentState
from services.ai.agents.drilling_data_agent.prompts import GENERATE_RESPONSE_PROMPT
from langchain_core.messages import AIMessage
from services.ai.common.models import get_llm
from common.logging import logger

llm = get_llm()


def generate_response_node(state: DrillAgentState) -> DrillAgentState:
    """Format execution result into natural language"""
    logger.info(
        f"[NODE] Starting generate_response_node for user {state.get('user_id')}"
    )

    prompt = GENERATE_RESPONSE_PROMPT.invoke(
        {
            "execution_result": state["execution_result"],
            "metadata": state["metadata"],
            "messages": state["messages"],
        }
    )

    response = llm.invoke(prompt)

    logger.info(
        f"[NODE] Completed generate_response_node - response length: {len(response.content)} chars"
    )

    return {
        "final_response": response.content,
        "messages": [AIMessage(content=response.content)],
    }
