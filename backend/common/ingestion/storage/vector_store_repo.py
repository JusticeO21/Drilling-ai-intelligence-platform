from common.ingestion.embeddings.embedding_service import EmbeddingService
from datetime import datetime
from typing import List, Optional
import json
from common.chroma_client import get_chroma_client
from common.logging import logger

COLLECTION_NAME = "drill_data_metadata"
DATASET_TYPE = "dataset"
COMPLEX_FIELDS = [
    "columns",
    "column_types",
    "numeric_columns",
    "categorical_columns",
    "datetime_columns",
    "percentage_columns",
    "id_columns",
]

COLUMN_STAT_FIELDS = [
    "count",
    "total_rows",
    "null_count",
    "null_percentage",
    "unique_count",
    "mean",
    "median",
    "std",
    "variance",
    "min",
    "max",
    "range",
    "q25",
    "q75",
    "skewness",
    "kurtosis",
    "top_value",
    "top_value_freq",
    "top_value_percentage",
    "true_count",
    "false_count",
    "true_percentage",
    "min_date",
    "max_date",
    "date_range_days",
]


def clean_metadata(metadata: dict) -> dict:
    """Remove None values from metadata."""
    return {k: v for k, v in metadata.items() if v is not None}


def serialize_complex_fields(metadata: dict) -> dict:
    """Convert lists/dicts to JSON strings for ChromaDB compatibility."""
    for field in COMPLEX_FIELDS:
        if field in metadata and metadata[field] is not None:
            metadata[field] = json.dumps(metadata[field])
    return metadata


def deserialize_complex_fields(metadata: dict) -> dict:
    """Convert JSON strings back to Python objects."""
    for field in COMPLEX_FIELDS:
        if field in metadata and isinstance(metadata[field], str):
            metadata[field] = json.loads(metadata[field])
    return metadata


def extract_column_stats(metadata: dict) -> dict:
    """Extract statistics from metadata into organized dict."""
    return {field: metadata.get(field) for field in COLUMN_STAT_FIELDS}


def build_user_filter(
    user_id: str, dataset_id: Optional[str] = None, include_dataset: bool = False
) -> dict:
    """Build filter conditions for ChromaDB queries."""
    conditions = [{"user_id": {"$eq": user_id}}]

    if dataset_id:
        conditions.append({"dataset_id": {"$eq": dataset_id}})

    if not include_dataset:
        conditions.append({"type": {"$ne": DATASET_TYPE}})

    return {"$and": conditions}


class VectorStoreRepository:
    """Manages storage and retrieval of dataset/column metadata in vector DB."""

    def __init__(self, client=None):
        try:
            if client is None:
                self.client = get_chroma_client()
            else:
                self.client = client
        except Exception as e:
            logger.error(f"Failed to initialize Chroma client: {e}")
            raise

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Collection for storing drilling data metadata"},
        )
        self.embed_model = EmbeddingService()

    def store_column_metadata(
        self,
        dataset_id: str,
        user_id: str,
        col: str,
        col_type: str,
        stats: dict,
        description: str,
    ):
        """Store column metadata with embeddings for semantic search."""
        embedding = self.embed_model.embed(description)

        metadata = {
            "dataset_id": dataset_id,
            "user_id": user_id,
            "column": col,
            "type": col_type,
            "description": description,
            "indexed_at": stats.get("indexed_at", datetime.utcnow().isoformat()),
            **{field: stats.get(field) for field in COLUMN_STAT_FIELDS},
        }

        self.collection.upsert(
            ids=[f"{dataset_id}:{col}"],
            embeddings=[embedding],
            metadatas=[clean_metadata(metadata)],
        )

    def store_dataset_metadata(
        self,
        dataset_id: str,
        user_id: str,
        dataset_name: str,
        dataset_stats: dict,
        description: str,
    ):
        """Store dataset-level metadata for queries like 'what datasets do I have?'"""
        embedding = self.embed_model.embed(description)

        metadata = {
            "dataset_id": dataset_id,
            "user_id": user_id,
            "type": DATASET_TYPE,
            "dataset_name": dataset_name,
            "description": description,
            "num_rows": dataset_stats.get("num_rows", 0),
            "num_cols": dataset_stats.get("num_cols", 0),
            "memory_usage_mb": dataset_stats.get("memory_usage_mb"),
            "total_null_cells": dataset_stats.get("total_null_cells", 0),
            "overall_null_percentage": dataset_stats.get(
                "overall_null_percentage", 0.0
            ),
            "complete_rows": dataset_stats.get("complete_rows", 0),
            "complete_rows_percentage": dataset_stats.get(
                "complete_rows_percentage", 0.0
            ),
            "duplicate_rows": dataset_stats.get("duplicate_rows", 0),
            "duplicate_rows_percentage": dataset_stats.get(
                "duplicate_rows_percentage", 0.0
            ),
            "indexed_at": dataset_stats.get(
                "indexed_at", datetime.utcnow().isoformat()
            ),
            **{field: dataset_stats.get(field, []) for field in COMPLEX_FIELDS},
        }

        metadata = serialize_complex_fields(clean_metadata(metadata))

        self.collection.upsert(
            ids=[f"{dataset_id}:_dataset"], embeddings=[embedding], metadatas=[metadata]
        )

    def store_full_profile(self, dataset_id: str, user_id: str, full_profile: dict):
        """Store complete profile from DataFrameProfiler."""
        self.store_dataset_metadata(
            dataset_id=dataset_id,
            user_id=user_id,
            dataset_name=full_profile["dataset"]["dataset_name"],
            dataset_stats=full_profile["dataset"],
            description=full_profile["dataset"]["description"],
        )

        for col_stats in full_profile["columns"]:
            self.store_column_metadata(
                dataset_id=dataset_id,
                user_id=user_id,
                col=col_stats["column"],
                col_type=col_stats["type"],
                stats=col_stats,
                description=col_stats["description"],
            )

    def retrieve_metadata(
        self,
        query: str,
        user_id: str,
        dataset_id: Optional[str] = None,
        top_k: int = 5,
        min_score: float = 0.4,
    ) -> dict:
        """
        Retrieve relevant column/dataset metadata for a user's query.

        Performs semantic search with score filtering and user isolation.
        """
        dataset_info = self._fetch_dataset_info(user_id, dataset_id)

        if dataset_info:
            dataset_info = deserialize_complex_fields(dataset_info)

        # 2. Search for relevant columns only
        query_embedding = self.embed_model.embed(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            where={
                "$and": [
                    {"user_id": {"$eq": user_id}},
                    {"dataset_id": {"$eq": dataset_id}},
                    {"type": {"$ne": DATASET_TYPE}},  # Exclude dataset from search
                ]
            },
            n_results=top_k,
            include=["metadatas", "distances"],
        )

        # 3. Process columns with score filtering
        columns = []
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for i, metadata in enumerate(metadatas):
            score = 1 - distances[i]
            if score >= min_score:
                columns.append(
                    {
                        "column": metadata.get("column"),
                        "type": metadata.get("type"),
                        "description": metadata.get("description"),
                        "stats": extract_column_stats(metadata),
                        "relevance_score": score,
                    }
                )

        return {"dataset": dataset_info, "columns": columns, "query": query}

    def _fetch_dataset_info(self, user_id: str, dataset_id: str) -> Optional[dict]:
        """Fetch dataset-level metadata directly by ID."""
        try:
            result = self.collection.get(
                ids=[f"{dataset_id}:_dataset"], include=["metadatas"]
            )

            dataset_key = f"{dataset_id}:_dataset"
            if result and dataset_key in result.get("ids", []):
                index = result["ids"].index(dataset_key)
                metadata = result["metadatas"][index]

                if metadata.get("user_id") == user_id:
                    return deserialize_complex_fields(metadata)

            return None
        except Exception as e:
            print(f"Error fetching dataset info: {e}")
            return None

    def list_user_datasets(self, user_id: str) -> List[dict]:
        """List all datasets belonging to a user with metadata."""
        query_embedding = self.embed_model.embed("list all datasets")

        results = self.collection.query(
            query_embeddings=[query_embedding],
            where={"user_id": {"$eq": user_id}, "type": {"$eq": DATASET_TYPE}},
            n_results=100,
            include=["metadatas"],
        )

        datasets = []
        metadatas = (
            results.get("metadatas", [[]])[0] if results.get("metadatas") else []
        )

        for metadata in metadatas:
            metadata = deserialize_complex_fields(metadata)
            datasets.append(
                {
                    "dataset_id": metadata.get("dataset_id"),
                    "dataset_name": metadata.get("dataset_name"),
                    "num_rows": metadata.get("num_rows"),
                    "num_cols": metadata.get("num_cols"),
                    "columns": metadata.get("columns"),
                    "memory_usage_mb": metadata.get("memory_usage_mb"),
                    "overall_null_percentage": metadata.get("overall_null_percentage"),
                    "complete_rows_percentage": metadata.get(
                        "complete_rows_percentage"
                    ),
                    "indexed_at": metadata.get("indexed_at"),
                }
            )

        return datasets
