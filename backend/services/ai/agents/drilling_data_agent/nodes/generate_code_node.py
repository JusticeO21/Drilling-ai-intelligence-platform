from services.ai.agents.drilling_data_agent.state import DrillAgentState
from services.ai.agents.drilling_data_agent.prompts import GENERATE_CODE_PROMPT
from langchain_core.messages import AIMessage
from services.ai.common.models import get_llm
from common.logging import logger

llm = get_llm()


def generate_code_node(state: DrillAgentState) -> DrillAgentState:
    """Generate Python code for DataFrame operations"""
    logger.info(f"[NODE] Starting generate_code_node for user {state.get('user_id')}")

    dataset_info = state["metadata_dict"].get("dataset") or {}

    prompt = GENERATE_CODE_PROMPT.invoke(
        {
            "columns": dataset_info.get("columns", []),
            "column_types": dataset_info.get("column_types", {}),
            "num_rows": dataset_info.get("num_rows", 0),
            "messages": state["messages"],
        }
    )

    response = llm.invoke(prompt)
    code = response.content.strip()
    print("CODE::::\n")
    print(code)

    # Clean up any markdown artifacts
    code = code.replace("```python", "").replace("```", "").strip()

    logger.info(
        f"[NODE] Completed generate_code_node - generated {len(code)} chars of code"
    )

    return {"python_code": code, "messages": [AIMessage(content=f"[Generated code]")]}
