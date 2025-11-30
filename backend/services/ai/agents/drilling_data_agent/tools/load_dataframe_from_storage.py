import pandas as pd
from common.ingestion.storage.redis_store_repo import RedisStoreRepository


def load_dataframe_from_storage(dataset_id: str) -> pd.DataFrame:
    """
    Load DataFrame from Redis storage using RedisStoreRepository.
    """
    try:
        redis_repo = RedisStoreRepository()
        return redis_repo.load_dataframe(dataset_id)

    except Exception as e:
        print(f"Error loading DataFrame: {e}")
        return None
