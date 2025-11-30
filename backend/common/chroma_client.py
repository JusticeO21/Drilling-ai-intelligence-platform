import chromadb
from common.config import settings
import logging

logger = logging.getLogger(__name__)


def get_chroma_client():
    """
    Factory function that returns the appropriate ChromaDB client
    based on CHROMA_MODE environment variable.

    Returns:
        chromadb.Client: Configured ChromaDB client (local or cloud)
    """
    mode = settings.chroma_mode.lower()

    try:
        if mode == "cloud":
            logger.info("Connecting to Chroma Cloud...")

            # Validate required cloud credentials
            missing = []
            if not settings.chroma_cloud_tenant:
                missing.append("CHROMA_CLOUD_TENANT")
            if not settings.chroma_cloud_database:
                missing.append("CHROMA_CLOUD_DATABASE")
            if not settings.chroma_api_token:
                missing.append("CHROMA_API_TOKEN")

            if missing:
                raise ValueError(
                    f"Chroma Cloud mode requires these env variables: {', '.join(missing)}"
                )

            client = chromadb.HttpClient(
                host="api.trychroma.com",
                port=443,
                ssl=True,
                headers={"X-Chroma-Token": settings.chroma_api_token},
                tenant=settings.chroma_cloud_tenant,
                database=settings.chroma_cloud_database,
            )

            # Test connection
            client.heartbeat()
            logger.info(
                f"Connected to Chroma Cloud "
                f"(tenant: {settings.chroma_cloud_tenant}, "
                f"database: {settings.chroma_cloud_database})"
            )

        elif mode == "local":
            logger.info(
                f"Connecting to local ChromaDB at {settings.chroma_host}:{settings.chroma_port}..."
            )

            # Initialize local client
            client = chromadb.HttpClient(
                host=settings.chroma_host, port=settings.chroma_port
            )

            client.heartbeat()
            logger.info(f"Connected to local ChromaDB")

        else:
            raise ValueError(f"Invalid CHROMA_MODE: {mode}. Must be 'local' or 'cloud'")

        return client

    except Exception as e:
        logger.error(f"Failed to connect to ChromaDB ({mode} mode): {e}")
        raise ConnectionError(f"ChromaDB connection failed: {e}")


def test_chroma_connection():
    """
    Test function to verify ChromaDB connection works
    """
    try:
        client = get_chroma_client()
        collections = client.list_collections()
        logger.info(
            f"ChromaDB connection test passed! Found {len(collections)} collections"
        )
        return True
    except Exception as e:
        logger.error(f"ChromaDB connection test failed: {e}")
        return False
