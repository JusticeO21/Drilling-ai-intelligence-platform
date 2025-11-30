from common.ingestion.storage.redis_store_repo import RedisStoreRepository


def validate_session(session_id: str) -> bool:
    """
    Validates if a session exists by checking for the corresponding dataset in Redis.

    Args:
        session_id (str): The session identifier to validate.

    Returns:
        bool: True if the session exists, False otherwise.
    """
    try:
        redis_repo = RedisStoreRepository()
        dataset_id = f"df_{session_id}"
        return redis_repo.redis_client.exists(dataset_id) > 0
    except Exception:
        return False
