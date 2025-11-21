import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading
import time
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from .logging import logger


class RAGSession:
    def __init__(self, session_id: str, vector_store: Chroma):
        self.session_id = session_id
        self.vector_store = vector_store
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(hours=24)  # 24 hour TTL
        self.last_accessed = self.created_at

    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at

    def update_access(self):
        self.last_accessed = datetime.now()


class RAGSessionManager:
    def __init__(self, embedding_model: Optional[Embeddings] = None):
        self.embedder = embedding_model
        self.sessions: Dict[str, RAGSession] = {}
        self.cleanup_interval = 3600  # 1 hour
        self.persist_directory = "./chroma_db"
        self._start_cleanup_thread()

    def _start_cleanup_thread(self):
        """Start background thread for session cleanup"""
        def cleanup_worker():
            while True:
                time.sleep(self.cleanup_interval)
                self._cleanup_expired_sessions()

        thread = threading.Thread(target=cleanup_worker, daemon=True)
        thread.start()
        logger.info("RAG session cleanup thread started")

    def _cleanup_expired_sessions(self):
        """Remove expired sessions - LangChain Chroma handles persistence automatically"""
        expired_sessions = []
        for session_id, session in self.sessions.items():
            if session.is_expired():
                expired_sessions.append(session_id)
                logger.info(f"Cleaned up expired session: {session_id}")

        for session_id in expired_sessions:
            del self.sessions[session_id]

        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")

    def create_session(self, chunks: List[str]) -> str:
        """Create a new RAG session with processed chunks using LangChain Chroma"""
        session_id = str(uuid.uuid4())

        if not self.embedder:
            raise ValueError("Embedding model not provided")

        # Convert text chunks to Document objects
        documents = [Document(page_content=chunk) for chunk in chunks]

        # Create vector store using LangChain's Chroma.from_documents()
        persist_dir = f"{self.persist_directory}/session_{session_id}"
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embedder,
            persist_directory=persist_dir,
            collection_name=f"session_{session_id}"
        )

        session = RAGSession(session_id, vector_store)
        self.sessions[session_id] = session

        logger.info(f"Created RAG session: {session_id} with {len(chunks)} chunks")
        return session_id

    def query_session(self, session_id: str, question: str, n_results: int = 3) -> Dict:
        """Query a RAG session using LangChain Chroma"""
        if session_id not in self.sessions:
            raise ValueError("Session not found or expired")

        session = self.sessions[session_id]
        if session.is_expired():
            del self.sessions[session_id]
            raise ValueError("Session expired")

        session.update_access()

        try:
            # Use LangChain's similarity_search
            docs = session.vector_store.similarity_search_with_score(question, k=n_results)

            relevant_chunks = [doc.page_content for doc, score in docs]
            distances = [score for doc, score in docs]

            return {
                "session_id": session_id,
                "question": question,
                "relevant_chunks": relevant_chunks,
                "distances": distances
            }

        except Exception as e:
            logger.error(f"Error querying session {session_id}: {e}")
            raise

    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """Get information about a session"""
        if session_id not in self.sessions:
            return None

        session = self.sessions[session_id]
        if session.is_expired():
            return None

        return {
            "session_id": session_id,
            "created_at": session.created_at.isoformat(),
            "expires_at": session.expires_at.isoformat(),
            "last_accessed": session.last_accessed.isoformat()
        }


# Global instance - will be initialized by AI service
rag_manager: Optional[RAGSessionManager] = None


def initialize_rag_manager(embedding_model: Embeddings) -> RAGSessionManager:
    """Initialize the global RAG manager with embedding model"""
    global rag_manager
    if rag_manager is None:
        rag_manager = RAGSessionManager(embedding_model)
    return rag_manager
