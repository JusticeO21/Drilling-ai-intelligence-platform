import pandas as pd
import pickle
import base64
from typing import Optional, Any
from common.config import settings
from common.logging import logger
from common.redis_client import get_redis_client


class RedisStoreRepository:
    """
    Handles DataFrame storage and retrieval in Redis using pickle serialization.
    Supports both local Redis (redis-py) and Upstash Redis (REST).
    """

    def __init__(self, client: Any = None):
        try:
            self.redis_client = client or get_redis_client()
        except Exception as e:
            logger.error(f"Failed to initialize Redis client: {e}")
            raise

    def store_dataframe(
        self, dataset_id: str, df: pd.DataFrame, expire_seconds: Optional[int] = None
    ) -> bool:

        try:
            # Serialize DataFrame as base64 string
            serialized_df = pickle.dumps(df)
            encoded_data = base64.b64encode(serialized_df).decode("utf-8")

            if expire_seconds:
                self.redis_client.set(dataset_id, encoded_data, ex=expire_seconds)
            else:
                self.redis_client.set(dataset_id, encoded_data)

            logger.info(f"Stored DataFrame (id: {dataset_id}, rows: {len(df)})")
            return True

        except Exception as e:
            logger.error(f"Failed to store DataFrame (id: {dataset_id}): {e}")
            return False

    def load_dataframe(self, dataset_id: str) -> Optional[pd.DataFrame]:
        try:
            encoded_data = self.redis_client.get(dataset_id)
            if encoded_data is None:
                logger.warning(f"DataFrame not found (id: {dataset_id})")
                return None

            serialized_df = base64.b64decode(encoded_data)
            df = pickle.loads(serialized_df)

            logger.info(f"Loaded DataFrame (id: {dataset_id}, rows: {len(df)})")
            return df

        except Exception as e:
            logger.error(f"Failed to load DataFrame (id: {dataset_id}): {e}")
            raise

    def delete_dataset(self, dataset_id: str) -> bool:
        try:
            deleted = self.redis_client.delete(dataset_id)

            if isinstance(deleted, dict):
                deleted = deleted.get("result", 0)

            if deleted == 1:
                logger.info(f"Deleted dataset (id: {dataset_id})")
                return True

            logger.warning(f"Dataset not found for deletion (id: {dataset_id})")
            return False

        except Exception as e:
            logger.error(f"Failed to delete dataset (id: {dataset_id}): {e}")
            return False

    def exists(self, dataset_id: str) -> bool:
        try:
            exists = self.redis_client.exists(dataset_id)

            if isinstance(exists, dict):
                exists = exists.get("result", 0)

            return exists == 1

        except Exception as e:
            logger.error(f"Failed to check dataset existence (id: {dataset_id}): {e}")
            return False

    def get_ttl(self, dataset_id: str) -> Optional[int]:
        try:
            ttl = self.redis_client.ttl(dataset_id)

            if isinstance(ttl, dict):
                ttl = ttl.get("result", None)

            if ttl is None or ttl < 0:
                return None

            return ttl

        except Exception as e:
            logger.error(f"Failed to get TTL (id: {dataset_id}): {e}")
            return None
