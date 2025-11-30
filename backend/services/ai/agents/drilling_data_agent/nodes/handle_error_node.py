from langchain_core.output_parsers import StrOutputParser
from services.ai.agents.drilling_data_agent.state import DrillAgentState
from services.ai.agents.drilling_data_agent.prompts import ERROR_HANDLING_PROMPT
from langchain_core.messages import AIMessage
from services.ai.common.models import get_llm
from common.logging import logger

llm = get_llm()


def handle_error_node(state: DrillAgentState) -> DrillAgentState:
    """Handle execution errors gracefully"""
    error_msg = state.get("error", "Unknown error")
    logger.warning(
        f"[NODE] Starting handle_error_node for user {state.get('user_id')} - Error: {error_msg}"
    )

    prompt = ERROR_HANDLING_PROMPT.invoke(
        {
            "error": error_msg,
            "query": state["messages"][-1].content if state["messages"] else "",
            "code": state.get("python_code", "No code generated"),
            "messages": state["messages"],
        }
    )

    chain = llm | StrOutputParser()
    response = chain.invoke(prompt)

    logger.info(f"[NODE] Completed handle_error_node - generated error response")

    return {"final_response": response, "messages": [AIMessage(content=response)]}
