from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ..common.models import get_llm
from common.logging import logger


def create_conversation_chain():
    """Create a basic conversational chain"""

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful AI assistant. Engage in natural conversation and be informative.",
            ),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()
    return chain


def create_drilling_conversation_chain():
    """Create a specialized conversation chain for drilling topics"""

    llm = get_llm()

    system_prompt = """
    You are an expert oil drilling consultant and data analyst. You specialize in:
    - Well drilling operations and optimization
    - Equipment and technology recommendations
    - Cost analysis and efficiency improvements
    - Safety protocols and risk management
    - Industry best practices and standards

    Engage in natural conversation while providing expert insights. Be professional, accurate, and helpful.
    When discussing technical topics, explain concepts clearly.
    """

    prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", "{input}")]
    )

    chain = prompt | llm | StrOutputParser()
    return chain


class ConversationManager:
    """Manages multiple conversation sessions"""

    def __init__(self):
        self.conversations = {}
        logger.info("Initialized ConversationManager")

    def chat(
        self, session_id: str, message: str, conversation_type: str = "general"
    ) -> str:
        """Send a message to a conversation session"""

        try:
            # Create appropriate chain based on type
            if conversation_type == "drilling":
                chain = create_drilling_conversation_chain()
            else:
                chain = create_conversation_chain()

            response = chain.invoke({"input": message})

            logger.info(
                f"Processed message for session {session_id}: {message[:50]}..."
            )
            return response

        except Exception as e:
            logger.error(f"Error in conversation for session {session_id}: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"

    def clear_conversation(self, session_id: str, conversation_type: str = "general"):
        """Clear conversation history for a session (no-op since we don't store history)"""
        logger.info(f"Conversation clearing not needed for stateless chains")


# Global conversation manager
conversation_manager = ConversationManager()
