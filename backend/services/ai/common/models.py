from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from .config import ai_settings
from common.config import settings
from common.logging import logger


def get_llm():
    """Get LLM based on configured provider."""

    provider = settings.model_provider
    logger.info(f"Initializing LLM with provider: {provider}")

    if provider == "anthropic":
        if not ai_settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment")

        return ChatAnthropic(
            model=ai_settings.anthropic_model,
            anthropic_api_key=ai_settings.anthropic_api_key,
            temperature=ai_settings.anthropic_temperature,
            max_tokens=ai_settings.anthropic_max_tokens,
        )

    elif provider == "openai":
        if not ai_settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")

        return ChatOpenAI(
            model=ai_settings.openai_model,
            openai_api_key=ai_settings.openai_api_key,
            temperature=ai_settings.openai_temperature,
            max_tokens=ai_settings.openai_max_tokens,
        )

    elif provider == "ollama":
        return ChatOllama(
            model=ai_settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=ai_settings.ollama_temperature,
        )

    else:
        raise ValueError(f"Unknown provider: {provider}")


def get_embeddings():
    from langchain_voyageai import VoyageAIEmbeddings

    return VoyageAIEmbeddings(model=ai_settings.voyage_embedding_model)
