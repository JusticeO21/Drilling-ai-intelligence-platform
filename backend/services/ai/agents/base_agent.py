from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from ..common.models import get_llm
from ..common.config import ai_settings
from ..common.utils import retrieve_context, format_context_for_prompt, validate_session
from common.logging import logger


class BaseAgent(ABC):
    """Base class for AI agents with common functionality"""

    def __init__(self, name: str = "BaseAgent"):
        self.name = name
        self.llm = get_llm()
        self.system_prompt = self._get_system_prompt()
        logger.info(f"Initialized {self.name} with {ai_settings.model_provider} provider")

    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass

    def create_chain(self):
        """Create a basic conversational chain"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}")
        ])

        chain = (
            RunnablePassthrough()
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain

    def chat(self, message: str, session_id: Optional[str] = None, **kwargs) -> str:
        """Basic chat functionality"""
        try:
            chain = self.create_chain()
            response = chain.invoke({"input": message})
            logger.info(f"{self.name} processed message: {message[:50]}...")
            return response
        except Exception as e:
            logger.error(f"Error in {self.name} chat: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"

    @abstractmethod
    def process_with_context(self, query: str, session_id: str) -> str:
        """Process a query with RAG context - to be implemented by subclasses"""
        pass


class RAGAgent(BaseAgent):
    """Base agent with RAG capabilities"""

    def __init__(self, name: str = "RAGAgent"):
        super().__init__(name)

    def process_with_context(self, query: str, session_id: str) -> str:
        """Process query with retrieved context"""
        try:
            # Validate session
            if not validate_session(session_id):
                return "I'm sorry, but your data session has expired or is invalid. Please upload your data again."

            # Retrieve relevant context
            context = retrieve_context(session_id, query, ai_settings.rag_max_chunks)

            # Format for LLM
            formatted_prompt = format_context_for_prompt(context, query)

            # Get response
            response = self.chat(formatted_prompt)

            logger.info(f"{self.name} processed query with context for session {session_id}")
            return response

        except Exception as e:
            logger.error(f"Error in {self.name} RAG processing: {e}")
            return f"I apologize, but I encountered an error processing your request: {str(e)}"
