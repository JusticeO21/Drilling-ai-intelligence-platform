import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..schemas import drilling as drilling_schema
from common.logging import logger
from common import rag as rag_module
from common.chroma_client import get_chroma_client
from common.ingestion.ingestion_service import DataIngestionService
from common.ingestion.loaders.file_loader import StructuredFileLoader
from common.ingestion.cleaning.data_cleaner import DataCleaner
from common.ingestion.profiling.data_profiler import DataFrameProfiler
from common.ingestion.storage import VectorStoreRepository, RedisStoreRepository
import redis

router = APIRouter()


@router.post("/upload", response_model=drilling_schema.FileProcessingResponse)
async def upload_drilling_data(file: UploadFile = File(...)):
    if not file.filename.endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="File must be CSV or Excel")

    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name

        if file.filename.endswith(".csv"):
            file_type = "csv"
        else:
            file_type = "excel"

        if rag_module.rag_manager is None:
            logger.info("Initializing RAG manager for first use")
            try:
                loader = StructuredFileLoader()
                cleaner = DataCleaner()
                profiler = DataFrameProfiler
                chroma_client = get_chroma_client()
                vector_repo = VectorStoreRepository(client=chroma_client)
                redis_repo = RedisStoreRepository()

                ingestion_service = DataIngestionService(
                    loader=loader,
                    cleaner=cleaner,
                    profiler=profiler,
                    vector_repo=vector_repo,
                    redis_repo=redis_repo,
                )

                initialized_manager = rag_module.initialize_rag_manager(
                    ingestion_service
                )
                logger.info(
                    f"RAG manager initialized: {initialized_manager is not None}"
                )

            except Exception as e:
                logger.error(f"Failed to initialize RAG manager: {e}")
                raise

        logger.info("Creating session for file: {}".format(file.filename))
        session_id = rag_module.rag_manager.create_session(
            file_path=temp_file_path, dataset_name=file.filename
        )

        session_info = rag_module.rag_manager.get_session_info(session_id)

        response = {
            "filename": file.filename,
            "file_type": file_type,
            "num_columns": len(session_info["columns"]) if session_info else 0,
            "columns": session_info["columns"] if session_info else [],
            "session_id": session_id,
        }

        logger.info(f"Processed file {file.filename}, created session {session_id}")
        return response

    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@router.post("/query", response_model=drilling_schema.QueryResponse)
def query_drilling_data(query: drilling_schema.QueryRequest):
    try:
        if rag_module.rag_manager is None:
            logger.info("Initializing RAG manager for first use")
            loader = StructuredFileLoader()
            cleaner = DataCleaner()
            profiler = DataFrameProfiler
            redis_client = redis.Redis(
                host="localhost", port=6379, db=0, decode_responses=True
            )
            chroma_client = get_chroma_client()
            vector_repo = VectorStoreRepository(client=chroma_client)
            redis_repo = RedisStoreRepository(redis_client)

            ingestion_service = DataIngestionService(
                loader=loader,
                cleaner=cleaner,
                profiler=profiler,
                vector_repo=vector_repo,
                redis_repo=redis_repo,
            )

            rag_module.initialize_rag_manager(ingestion_service)

        result = rag_module.rag_manager.query_session(
            query.session_id, query.question, query.n_results
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error querying session {query.session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error querying data: {str(e)}")


@router.get("/session/{session_id}", response_model=drilling_schema.SessionInfo)
def get_session_info(session_id: str):
    if rag_module.rag_manager is None:
        logger.info("Initializing RAG manager for first use")

        loader = StructuredFileLoader()
        cleaner = DataCleaner()
        profiler = DataFrameProfiler
        redis_client = redis.Redis(
            host="localhost", port=6379, db=0, decode_responses=True
        )
        chroma_client = get_chroma_client()
        vector_repo = VectorStoreRepository(client=chroma_client)
        redis_repo = RedisStoreRepository(redis_client)

        ingestion_service = DataIngestionService(
            loader=loader,
            cleaner=cleaner,
            profiler=profiler,
            vector_repo=vector_repo,
            redis_repo=redis_repo,
        )

        rag_module.initialize_rag_manager(ingestion_service, redis_client)

    session_info = rag_module.rag_manager.get_session_info(session_id)
    if session_info is None:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    return session_info
