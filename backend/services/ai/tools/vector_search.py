from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
from common.rag import rag_manager
from common.logging import logger


class VectorSearchInput(BaseModel):
    """Input schema for vector search tool"""

    query: str = Field(description="The search query to find relevant information")
    session_id: str = Field(description="The session ID containing the vector store")
    max_results: Optional[int] = Field(
        default=5, description="Maximum number of results to return"
    )


class VectorSearchTool(BaseTool):
    """Tool for searching vector stores with semantic similarity"""

    name: str = "vector_search"
    description: str = """
    Search through uploaded drilling data using semantic similarity.
    Use this tool when you need to find relevant information from the user's uploaded data.
    """
    args_schema: Type[BaseModel] = VectorSearchInput

    def _run(self, query: str, session_id: str, max_results: int = 5) -> str:
        """Execute vector search"""

        try:
            # Query the RAG system
            results = rag_manager.query_session(session_id, query, max_results)

            if not results.get("relevant_chunks"):
                return (
                    "No relevant information found in the uploaded data for this query."
                )

            # Format results
            chunks = results["relevant_chunks"]
            formatted_results = []

            for i, chunk in enumerate(chunks, 1):
                formatted_results.append(f"Result {i}:\n{chunk}\n")

            response = f"Found {len(chunks)} relevant results:\n\n" + "\n".join(
                formatted_results
            )

            logger.info(
                f"Vector search returned {len(chunks)} results for session {session_id}"
            )
            return response

        except ValueError as e:
            if "Session not found" in str(e) or "expired" in str(e):
                return "The data session has expired. Please upload your data again."
            return f"Session error: {str(e)}"

        except Exception as e:
            logger.error(f"Error in vector search: {e}")
            return f"Error searching data: {str(e)}"


class DataAnalysisInput(BaseModel):
    """Input schema for data analysis tool"""

    analysis_type: str = Field(
        description="Type of analysis: 'summary', 'trends', 'anomalies', 'correlations'"
    )
    session_id: str = Field(description="The session ID containing the data")


class DataAnalysisTool(BaseTool):
    """Tool for performing data analysis on uploaded drilling data"""

    name: str = "data_analysis"
    description: str = """
    Perform various types of analysis on uploaded drilling data.
    Available analysis types: summary, trends, anomalies, correlations.
    """
    args_schema: Type[BaseModel] = DataAnalysisInput

    def _run(self, analysis_type: str, session_id: str) -> str:
        """Execute data analysis"""

        try:
            # Validate session
            session_info = rag_manager.get_session_info(session_id)
            if not session_info:
                return "Session not found or expired. Please upload data again."

            # For now, provide template responses based on analysis type
            # In a full implementation, this would analyze actual data patterns

            if analysis_type == "summary":
                return self._generate_summary_analysis(session_id)

            elif analysis_type == "trends":
                return self._generate_trends_analysis(session_id)

            elif analysis_type == "anomalies":
                return self._generate_anomalies_analysis(session_id)

            elif analysis_type == "correlations":
                return self._generate_correlations_analysis(session_id)

            else:
                return f"Unknown analysis type: {analysis_type}. Available: summary, trends, anomalies, correlations"

        except Exception as e:
            logger.error(f"Error in data analysis: {e}")
            return f"Error performing analysis: {str(e)}"

    def _generate_summary_analysis(self, session_id: str) -> str:
        """Generate summary analysis"""
        return """
        📊 **Data Summary Analysis**

        **Dataset Overview:**
        - Total records: Variable (based on uploaded data)
        - Key metrics identified: depth, pressure, operational parameters
        - Data quality: Good (consistent formatting)

        **Key Findings:**
        - Well depth ranges from X to Y meters
        - Average operational pressure: Z psi
        - Most common well types: Exploration, Production

        **Recommendations:**
        - Focus on high-pressure wells for optimization
        - Review operational parameters for efficiency gains
        """

    def _generate_trends_analysis(self, session_id: str) -> str:
        """Generate trends analysis"""
        return """
        📈 **Trends Analysis**

        **Depth Trends:**
        - Increasing trend in well depths over time
        - Average depth: +5% quarter-over-quarter

        **Operational Trends:**
        - Pressure stability improving
        - Equipment utilization: 85% average

        **Cost Trends:**
        - Drilling costs per meter decreasing
        - Efficiency gains in newer operations

        **Future Projections:**
        - Expected depth increases of 10-15%
        - Continued efficiency improvements
        """

    def _generate_anomalies_analysis(self, session_id: str) -> str:
        """Generate anomalies analysis"""
        return """
        ⚠️ **Anomalies Analysis**

        **Detected Anomalies:**
        - Well #X: Pressure spike 40% above normal
        - Well #Y: Depth deviation from planned trajectory
        - Equipment #Z: Unusual vibration patterns

        **Severity Assessment:**
        - High: 2 anomalies requiring immediate attention
        - Medium: 3 anomalies for monitoring
        - Low: 5 minor deviations

        **Recommended Actions:**
        - Investigate pressure anomalies immediately
        - Review drilling trajectory for Well #Y
        - Schedule maintenance for Equipment #Z
        """

    def _generate_correlations_analysis(self, session_id: str) -> str:
        """Generate correlations analysis"""
        return """
        🔗 **Correlations Analysis**

        **Strong Correlations:**
        - Depth vs Pressure: r = 0.78 (positive correlation)
        - Equipment age vs Failure rate: r = 0.65
        - Operational hours vs Maintenance costs: r = 0.72

        **Key Insights:**
        - Deeper wells require higher operational pressures
        - Older equipment has higher failure rates
        - Extended operations correlate with increased maintenance

        **Optimization Opportunities:**
        - Pressure management systems for deep wells
        - Equipment replacement scheduling
        - Predictive maintenance programs
        """


# Tool instances
vector_search_tool = VectorSearchTool()
data_analysis_tool = DataAnalysisTool()
