from typing import List, Dict, Any
from common import rag as rag_module
from common.logging import logger


def retrieve_context(session_id: str, query: str, max_chunks: int = 5) -> str:
    """Retrieve relevant context from RAG system"""
    try:
        results = rag_module.rag_manager.query_session(session_id, query, max_chunks)
        relevant_chunks = results.get("relevant_chunks", [])

        # Combine chunks into context string
        context = "\n\n".join(relevant_chunks)
        logger.info(f"Retrieved {len(relevant_chunks)} chunks for session {session_id}")
        return context

    except Exception as e:
        logger.error(f"Error retrieving context for session {session_id}: {e}")
        return ""


def format_context_for_prompt(context: str, query: str) -> str:
    """Format context and query for LLM prompt"""
    if not context:
        return f"User Query: {query}\n\nNo relevant data found in uploaded files."

    return f"""Based on the following data from uploaded files:

{context}

User Query: {query}

Please provide a helpful and accurate response based on the data above. If the data doesn't contain relevant information, please say so."""


def validate_session(session_id: str) -> bool:
    """Validate if a session exists and is active"""
    if rag_module.rag_manager is None:
        return False
    session_info = rag_module.rag_manager.get_session_info(session_id)
    return session_info is not None


def get_session_stats(session_id: str) -> Dict[str, Any]:
    """Get statistics about a session"""
    if rag_module.rag_manager is None:
        return {"error": "RAG system not initialized"}

    session_info = rag_module.rag_manager.get_session_info(session_id)
    if not session_info:
        return {"error": "Session not found"}

    return {
        "session_id": session_id,
        "created_at": session_info["created_at"],
        "expires_at": session_info["expires_at"],
        "last_accessed": session_info["last_accessed"],
        "is_active": True,
    }
