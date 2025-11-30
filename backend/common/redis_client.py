import redis
from upstash_redis import Redis as UpstashRedis
from common.config import settings
from common.logging import logger


def get_redis_client():
    """
    Factory function to return local Redis (TCP) or Upstash (REST)
    depending on REDIS_MODE.
    """
    mode = settings.redis_mode.lower()

    try:
        if mode == "cloud":
            logger.info("Connecting to Upstash Redis...")

            if not settings.upstash_redis_url or not settings.upstash_redis_token:
                raise ValueError(
                    "Upstash mode requires UPSTASH_REDIS_URL and UPSTASH_REDIS_TOKEN"
                )

            client = UpstashRedis(
                url=settings.upstash_redis_url,
                token=settings.upstash_redis_token,
            )

            client.set("healthcheck", "ok")
            logger.info("Connected to Upstash Redis.")
            return client

        elif mode == "local":
            logger.info(
                f"Connecting to local Redis at {settings.redis_host}:{settings.redis_port}..."
            )

            client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password,
                decode_responses=True,
            )

            client.ping()
            logger.info("Connected to local Redis.")
            return client

        else:
            raise ValueError(f"Invalid REDIS_MODE: {mode}. Use 'local' or 'cloud'.")

    except Exception as e:
        logger.error(f"Redis connection error ({mode}): {e}")
        raise ConnectionError(f"Redis connection failed: {e}")
