from langchain_voyageai import VoyageAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from common.config import settings
from common.logging import logger


class EmbeddingService:
    def __init__(self):
        if settings.embedding_provider != "ollama":
            logger.info("Initializing Voyage embeddings")
            self.model = VoyageAIEmbeddings(model=settings.voyage_embedding_model)
        else:
            self.model = OllamaEmbeddings(
                model=settings.ollama_embedding_model, base_url=settings.ollama_base_url
            )

    def embed(self, text: str):
        return self.model.embed_query(text)
