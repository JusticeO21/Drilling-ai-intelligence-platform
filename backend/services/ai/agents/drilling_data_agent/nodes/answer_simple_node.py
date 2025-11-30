from services.ai.agents.drilling_data_agent.state import DrillAgentState
from services.ai.agents.drilling_data_agent.prompts import ANSWER_SIMPLE_PROMPT
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from services.ai.common.models import get_llm
from common.logging import logger

llm = get_llm()


def answer_simple_node(state: DrillAgentState) -> DrillAgentState:
    """Answer from metadata only"""
    logger.info(f"[NODE] Starting answer_simple_node for user {state.get('user_id')}")

    prompt = ANSWER_SIMPLE_PROMPT.invoke(
        {"metadata": state["metadata"], "query": state["messages"][0]}
    )

    chain = llm | StrOutputParser()
    response = chain.invoke(prompt)

    logger.info(
        f"[NODE] Completed answer_simple_node - response length: {len(response)} chars"
    )

    return {"final_response": response, "messages": [AIMessage(content=response)]}
