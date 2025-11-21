from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from ..common.models import get_llm
from ..common.utils import retrieve_context
from common.logging import logger


def create_rag_chain(session_id: str):
    """Create a RAG chain for question answering with context"""

    llm = get_llm()

    # RAG prompt template
    rag_prompt = ChatPromptTemplate.from_template(
        """
You are an expert oil drilling data analyst. Use the following context from uploaded drilling data to answer the user's question.

Context from uploaded data:
{context}

Question: {question}

Instructions:
- Answer based primarily on the provided context
- Be specific and reference actual data when possible
- If the context doesn't contain relevant information, say so clearly
- Provide actionable insights when appropriate
- Keep responses focused and professional

Answer:"""
    )

    def retrieve_and_format(query: str) -> str:
        """Retrieve context and format for the prompt"""
        try:
            context = retrieve_context(session_id, query)
            logger.info(
                f"Retrieved context for session {session_id}: {len(context)} chars"
            )
            return context
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return "Error retrieving context from uploaded data."

    rag_chain = (
        RunnablePassthrough.assign(context=lambda x: retrieve_and_format(x["question"]))
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def create_conversational_rag_chain(session_id: str, chat_history: list = None):
    """Create a conversational RAG chain that maintains chat history"""

    llm = get_llm()

    # Conversational RAG prompt
    conversational_prompt = ChatPromptTemplate.from_template(
        """
You are an expert oil drilling data analyst having a conversation with a user about their drilling data.

Previous conversation:
{chat_history}

Context from uploaded drilling data:
{context}

Current question: {question}

Instructions:
- Use both the conversation history and data context to provide relevant answers
- Reference previous parts of the conversation when appropriate
- Build upon previous explanations or analyses
- Ask clarifying questions if needed
- Maintain continuity in your analysis

Answer:"""
    )

    def format_chat_history(history: list) -> str:
        """Format chat history for the prompt"""
        if not history:
            return "No previous conversation."

        formatted = []
        for msg in history[-5:]:
            formatted.append(f"User: {msg.get('user', '')}")
            formatted.append(f"Assistant: {msg.get('assistant', '')}")

        return "\n".join(formatted)

    def retrieve_and_format(query: str) -> str:
        """Retrieve context and format for the prompt"""
        try:
            context = retrieve_context(session_id, query)
            return context
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return "Error retrieving context from uploaded data."

    chain = (
        RunnablePassthrough.assign(
            context=lambda x: retrieve_and_format(x["question"]),
            chat_history=lambda x: format_chat_history(x.get("chat_history", [])),
        )
        | conversational_prompt
        | llm
        | StrOutputParser()
    )

    return chain
