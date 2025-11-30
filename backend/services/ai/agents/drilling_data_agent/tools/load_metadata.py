from common.ingestion.storage.vector_store_repo import VectorStoreRepository
from common.chroma_client import get_chroma_client


def extract_metadata(query: str, user_id: str, dataset_id: str):
    chroma_client = get_chroma_client()
    vector_store = VectorStoreRepository(client=chroma_client)

    return vector_store.retrieve_metadata(
        query=query,
        user_id=user_id,
        dataset_id=dataset_id,
        top_k=5,
    )
