import uuid
import json
from common.logging import logger
from common.chroma_client import get_chroma_client
from datetime import datetime, timedelta
from typing import Dict, Optional
from .ingestion.ingestion_service import DataIngestionService
from .ingestion.storage.vector_store_repo import VectorStoreRepository
from common.redis_client import get_redis_client


class RAGSessionManager:
    def __init__(self, ingestion_service: DataIngestionService):
        self.ingestion_service = ingestion_service

        try:
            self.chroma_client = get_chroma_client()
        except Exception as e:
            logger.error(f"Failed to initialize Chroma client: {e}")
            raise

        try:
            self.redis_client = get_redis_client()
        except Exception as e:
            logger.error(f"Failed to initialize Redis client: {e}")
            raise

        self.vector_repo = VectorStoreRepository(client=self.chroma_client)

    def create_session(
        self,
        dataframe=None,
        file_path: str = None,
        user_id: str = None,
        dataset_name: str = None,
    ) -> str:
        """Create a new session by ingesting structured data"""
        # Auto-generate user_id for open system
        if user_id is None:
            user_id = str(uuid.uuid4())
            logger.info(f"Created data session: {user_id}")

        # Use ingestion service to process the data
        result = self.ingestion_service.ingest(
            dataframe=dataframe,
            file_path=file_path,
            user_id=user_id,
            dataset_id=f"df_{user_id}",
            dataset_name=dataset_name,
        )

        dataset_id = result["dataset_id"]
        session_id = user_id  # session_id = user_id for open system
        session_data = {
            "user_id": user_id,
            "dataset_id": dataset_id,
            "created_at": datetime.now().isoformat(),
            "dataset_name": dataset_name,
            "columns": result["columns"],
        }

        try:
            self.redis_client.setex(
                f"session:{session_id}", 86400, json.dumps(session_data)
            )
        except Exception as e:
            logger.error(f"Failed to store session metadata (id: {session_id}): {e}")
            raise

        logger.info(f"Created data session: {session_id} (dataset: {dataset_id})")
        return session_id

    def query_session(self, session_id: str, question: str, n_results: int = 5) -> Dict:
        """Query a session using structured data retrieval"""
        session_data = self.redis_client.get(f"session:{session_id}")
        if not session_data:
            raise ValueError("Session not found or expired")

        session = json.loads(session_data)

        try:
            results = self.vector_repo.retrieve_metadata(
                query=question,
                user_id=session_id,
                dataset_id=session["dataset_id"],
                top_k=n_results,
            )

            return {
                "session_id": session_id,
                "question": question,
                "columns": results["columns"],
                "dataset": results["dataset"],
                "query": results["query"],
            }

        except Exception as e:
            logger.error(f"Error querying session {session_id}: {e}")
            raise

    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """Get information about a session"""
        session_data = self.redis_client.get(f"session:{session_id}")
        if not session_data:
            return None

        session = json.loads(session_data)

        ttl = self.redis_client.ttl(f"session:{session_id}")
        expires_at = datetime.now() + timedelta(seconds=ttl)

        return {
            "session_id": session_id,
            "user_id": session["user_id"],
            "dataset_id": session["dataset_id"],
            "created_at": session["created_at"],
            "expires_at": expires_at.isoformat(),
            "dataset_name": session.get("dataset_name"),
            "columns": session["columns"],
        }


rag_manager: Optional[RAGSessionManager] = None


def initialize_rag_manager(
    ingestion_service: DataIngestionService,
) -> RAGSessionManager:
    """Initialize the global RAG manager with ingestion service and Redis"""
    global rag_manager
    if rag_manager is None:
        rag_manager = RAGSessionManager(ingestion_service)
    return rag_manager
