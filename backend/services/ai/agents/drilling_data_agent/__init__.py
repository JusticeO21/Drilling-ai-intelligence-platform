from .graph import create_drill_agent_workflow
from .state import DrillAgentState
from typing import Dict, Any, AsyncGenerator
from common.logging import logger

WORKFLOW_STAGES = {
    "extracting": "Extracting data insights...",
    "analyzing": "Analyzing query complexity...",
    "simple_response": "Generating direct answer...",
    "complex_code": "Creating analysis code...",
    "complex_analysis": "Running data analysis...",
    "complex_format": "Formatting final response...",
}


class DrillingDataAgent:
    """Drilling data analysis agent with LangGraph workflow."""

    def __init__(self):
        self.workflow = create_drill_agent_workflow()

    def analyze_query(self, state: DrillAgentState) -> Dict[str, Any]:
        return self.workflow.invoke(state)

    async def analyze_query_async(self, state: DrillAgentState) -> Dict[str, Any]:
        return await self.workflow.ainvoke(state)

    async def stream_analyze_query(
        self, state: DrillAgentState
    ) -> AsyncGenerator[Dict[str, str], None]:
        """Stream workflow execution with informative status messages."""
        try:
            async for partial_state in self.workflow.astream(
                state, stream_mode="values"
            ):
                messages = self._process_workflow_stage(partial_state)
                for message in messages:
                    yield message

                if "final_response" in partial_state:
                    break

        except Exception as e:
            logger.error(f"Workflow streaming error: {e}", exc_info=True)
            yield {"type": "error", "message": "Processing failed. Please try again."}

    def _process_workflow_stage(
        self, partial_state: Dict[str, Any]
    ) -> list[Dict[str, str]]:
        """Process workflow stage and return appropriate status messages."""
        has_metadata = "metadata" in partial_state
        has_query_type = "query_type" in partial_state
        has_final_response = "final_response" in partial_state

        if has_final_response:
            return [{"type": "content", "delta": partial_state["final_response"]}]

        if has_query_type and not has_final_response:
            query_type = partial_state["query_type"]
            return self._get_query_type_messages(query_type)

        if has_metadata and not has_query_type:
            return [{"type": "status", "message": WORKFLOW_STAGES["extracting"]}]

        return []

    def _get_query_type_messages(self, query_type: str) -> list[Dict[str, str]]:
        """Get status messages based on query type."""
        base_message = {"type": "status", "message": WORKFLOW_STAGES["analyzing"]}

        if query_type == "simple":
            return [
                base_message,
                {"type": "status", "message": WORKFLOW_STAGES["simple_response"]},
            ]

        return [
            base_message,
            {"type": "status", "message": WORKFLOW_STAGES["complex_code"]},
            {"type": "status", "message": WORKFLOW_STAGES["complex_analysis"]},
            {"type": "status", "message": WORKFLOW_STAGES["complex_format"]},
        ]
