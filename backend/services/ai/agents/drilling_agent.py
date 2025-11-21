from .base_agent import RAGAgent
from ..common.config import ai_settings
from common.logging import logger


class DrillingAgent(RAGAgent):
    """Specialized agent for oil drilling data analysis and Q&A"""

    def __init__(self):
        super().__init__("DrillingAgent")

    def _get_system_prompt(self) -> str:
        """Return specialized system prompt for drilling data"""
        return """You are an expert oil drilling data analyst and consultant. You help users understand and analyze drilling data, well information, and operational metrics with not too long responses and not too complex.

Your expertise includes:
- Well performance analysis
- Drilling efficiency metrics
- Cost analysis and optimization
- Safety and risk assessment
- Equipment and technology recommendations
- Industry best practices

When analyzing data:
1. Be precise and data-driven in your responses
2. Explain technical terms when using them
3. Provide actionable insights when possible
4. Acknowledge limitations in the data
5. Suggest follow-up questions or analyses when relevant

Always maintain a professional, helpful, and accurate tone. If you're unsure about something, admit it rather than making assumptions."""

    def process_drilling_query(self, query: str, session_id: str) -> str:
        """Process drilling-specific queries with enhanced context"""
        try:
            # Add drilling-specific context enhancement
            enhanced_query = self._enhance_drilling_query(query)

            # Use parent RAG processing
            response = self.process_with_context(enhanced_query, session_id)

            # Post-process response for drilling context
            response = self._post_process_drilling_response(response, query)

            return response

        except Exception as e:
            logger.error(f"Error in drilling query processing: {e}")
            return f"I apologize, but I encountered an error analyzing your drilling data: {str(e)}"

    def _enhance_drilling_query(self, query: str) -> str:
        """Enhance user queries with drilling-specific context"""
        drilling_keywords = [
            "well",
            "drill",
            "depth",
            "pressure",
            "mud",
            "casing",
            "bit",
            "formation",
            "reservoir",
            "production",
            "cost",
            "efficiency",
            "safety",
            "equipment",
            "optimization",
        ]

        query_lower = query.lower()
        has_drilling_context = any(
            keyword in query_lower for keyword in drilling_keywords
        )

        if not has_drilling_context:
            # Add context hint for better retrieval
            enhanced = f"Drilling/Oil well context: {query}"
            logger.info(f"Enhanced query for better retrieval: {enhanced}")
            return enhanced

        return query

    def _post_process_drilling_response(
        self, response: str, original_query: str
    ) -> str:
        """Post-process responses with drilling-specific formatting and suggestions"""
        # Add helpful suggestions based on query type
        query_lower = original_query.lower()

        if "cost" in query_lower or "budget" in query_lower:
            response += "\n\n💡 **Cost Analysis Tip**: Consider reviewing drilling efficiency metrics and equipment utilization rates for optimization opportunities."

        elif "safety" in query_lower or "risk" in query_lower:
            response += "\n\n⚠️ **Safety Note**: Always prioritize safety protocols and ensure compliance with industry standards and regulations."

        elif "optimization" in query_lower or "efficiency" in query_lower:
            response += "\n\n🔧 **Optimization Suggestion**: Look into real-time monitoring systems and predictive analytics for continuous improvement."

        elif "depth" in query_lower or "pressure" in query_lower:
            response += "\n\n📊 **Technical Note**: Monitor pressure gradients and formation integrity throughout the drilling process."

        return response

    def get_drilling_insights(self, session_id: str) -> str:
        """Provide general insights about the uploaded drilling data"""
        insight_prompt = """
        Based on the drilling data provided, please provide:
        1. A summary of key metrics and trends
        2. Any notable patterns or anomalies
        3. Potential areas for optimization
        4. Recommendations for further analysis

        Focus on being concise but comprehensive.
        """

        return self.process_with_context(insight_prompt, session_id)
