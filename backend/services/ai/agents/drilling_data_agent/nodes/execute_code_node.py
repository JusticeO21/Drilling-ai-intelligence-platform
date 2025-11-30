import pandas as pd
from services.ai.agents.drilling_data_agent.state import DrillAgentState
from services.ai.agents.drilling_data_agent.tools import (
    load_dataframe_from_storage,
    execute_python_with_timeout,
)
from langchain_core.messages import AIMessage
from common.logging import logger


def execute_code_node(state: DrillAgentState) -> DrillAgentState:
    """
    Safely execute generated Python code on the DataFrame.
    """
    logger.info(
        f"[NODE] Starting execute_code_node for dataset {state.get('dataset_id')}"
    )

    try:
        df = load_dataframe_from_storage(state["dataset_id"])

        if df is None or df.empty:
            logger.warning(
                f"[NODE] DataFrame not found or empty for dataset {state.get('dataset_id')}"
            )
            return {
                "error": "DataFrame not found or empty",
                "execution_result": None,
                "messages": [
                    AIMessage(content="[Execution failed: DataFrame not found]")
                ],
            }

        logger.info(f"[NODE] Loaded DataFrame with {len(df)} rows, executing code...")
        result = execute_python_with_timeout(
            code=state["python_code"], context={"df": df, "pd": pd}
        )

        logger.info(f"[NODE] Completed execute_code_node successfully")
        return {
            "execution_result": result,
            "messages": [AIMessage(content="[Code executed successfully]")],
        }

    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"[NODE] execute_code_node failed: {error_msg}")
        return {
            "error": error_msg,
            "execution_result": None,
            "messages": [AIMessage(content=f"[Execution error: {error_msg}]")],
        }
