from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_core.language_models import BaseLanguageModel
from langchain_core.embeddings import Embeddings
from .config import ai_settings
from common.logging import logger


def get_llm() -> BaseLanguageModel:
    """Factory function to get the appropriate LLM based on configuration"""

    if ai_settings.model_provider == "openai":
        if not ai_settings.openai_api_key:
            raise ValueError("OpenAI API key is required when using OpenAI provider")

        logger.info(f"Initializing OpenAI model: {ai_settings.openai_model}")
        return ChatOpenAI(
            api_key=ai_settings.openai_api_key,
            model=ai_settings.openai_model,
            temperature=ai_settings.openai_temperature,
            max_tokens=ai_settings.openai_max_tokens,
        )

    elif ai_settings.model_provider == "ollama":
        logger.info(f"Initializing Ollama model: {ai_settings.ollama_model} at {ai_settings.ollama_base_url}")
        return ChatOllama(
            base_url=ai_settings.ollama_base_url,
            model=ai_settings.ollama_model,
            temperature=ai_settings.ollama_temperature,
            num_predict=ai_settings.ollama_max_tokens,
        )

    else:
        raise ValueError(f"Unsupported model provider: {ai_settings.model_provider}")


def get_embedding_model() -> Embeddings:
    """Get embedding model for vector operations using LangChain"""

    if ai_settings.model_provider == "openai":
        if not ai_settings.openai_api_key:
            raise ValueError("OpenAI API key is required for OpenAI embeddings")

        logger.info("Initializing OpenAI embeddings")
        return OpenAIEmbeddings(
            api_key=ai_settings.openai_api_key,
            model="text-embedding-3-small"
        )

    elif ai_settings.model_provider == "ollama":
        logger.info(f"Initializing Ollama embeddings with model: {ai_settings.ollama_embedding_model}")
        return OllamaEmbeddings(
            model=ai_settings.ollama_embedding_model,
        )

    else:
        raise ValueError(f"Unsupported model provider: {ai_settings.model_provider}")
