from langgraph.graph import StateGraph, END
from services.ai.agents.drilling_data_agent.state import DrillAgentState
from services.ai.agents.drilling_data_agent.nodes import (
    retrieve_metadata_node,
    classify_query_node,
    answer_simple_node,
    generate_code_node,
    generate_response_node,
    execute_code_node,
    handle_error_node,
)
from typing import Literal


def route_after_classification(
    state: DrillAgentState,
) -> Literal["answer_simple", "generate_code"]:
    """Route based on query complexity"""
    return "answer_simple" if state["query_type"] == "simple" else "generate_code"


def route_after_execution(
    state: DrillAgentState,
) -> Literal["generate_response", "handle_error"]:
    """Route to error handler if execution failed"""
    return "handle_error" if state.get("error") else "generate_response"


def create_drill_agent_workflow():
    """Factory function for drilling data analysis workflow."""
    workflow = StateGraph(DrillAgentState)

    workflow.add_node("extract_metadata", retrieve_metadata_node)
    workflow.add_node("classify_query", classify_query_node)
    workflow.add_node("answer_simple", answer_simple_node)
    workflow.add_node("generate_code", generate_code_node)
    workflow.add_node("execute_code", execute_code_node)
    workflow.add_node("generate_response", generate_response_node)
    workflow.add_node("handle_error", handle_error_node)

    workflow.set_entry_point("extract_metadata")
    workflow.add_edge("extract_metadata", "classify_query")
    workflow.add_conditional_edges(
        "classify_query",
        route_after_classification,
        {"answer_simple": "answer_simple", "generate_code": "generate_code"},
    )
    workflow.add_edge("answer_simple", END)
    workflow.add_edge("generate_code", "execute_code")

    workflow.add_conditional_edges(
        "execute_code",
        route_after_execution,
        {"generate_response": "generate_response", "handle_error": "handle_error"},
    )
    workflow.add_edge("generate_response", END)
    workflow.add_edge("handle_error", END)

    return workflow.compile()
