from services.ai.agents.drilling_data_agent.state import DrillAgentState
from services.ai.agents.drilling_data_agent.prompts import CLASSIFY_QUERY_PROMPT
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from services.ai.common.models import get_llm
from common.logging import logger

llm = get_llm()


def classify_query_node(state: DrillAgentState) -> DrillAgentState:
    """LLM classifies query as simple or complex"""
    logger.info(f"[NODE] Starting classify_query_node for user {state.get('user_id')}")

    # Invoke with prompt template
    prompt = CLASSIFY_QUERY_PROMPT.invoke(
        {"context": state["metadata"], "messages": state["messages"]}
    )
    logger.info(f"[NODE]-------------------------- Prompt: {prompt}")

    chain = llm | StrOutputParser()

    response = chain.invoke(prompt)
    classification = response.lower()

    logger.info(
        f"[NODE] Completed classify_query_node - classified as: {classification}"
    )

    return {
        "query_type": classification,
        "messages": [AIMessage(content=f"[Classification: {classification}]")],
    }
