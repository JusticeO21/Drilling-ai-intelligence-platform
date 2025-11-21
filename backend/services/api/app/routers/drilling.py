from fastapi import APIRouter, UploadFile, File, HTTPException
from ..schemas import drilling as drilling_schema
from common.logging import logger
from common import rag as rag_module
from services.ai.common.models import get_embedding_model
from services.ai.common.document_processor import process_file_for_rag

router = APIRouter()


@router.post("/upload", response_model=drilling_schema.FileProcessingResponse)
async def upload_drilling_data(file: UploadFile = File(...)):
    if not file.filename.endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="File must be CSV or Excel")

    try:
        contents = await file.read()

        # Use LangChain document processor for proper file handling
        rag_chunks = process_file_for_rag(contents, file.filename)

        # Determine file type for response
        if file.filename.endswith(".csv"):
            file_type = "csv"
        else:
            file_type = "excel"

        # Initialize RAG manager if not already done
        if rag_module.rag_manager is None:
            logger.info("Initializing RAG manager for first use")
            try:
                embedding_model = get_embedding_model()
                logger.info(f"Embedding model created: {type(embedding_model)}")
                initialized_manager = rag_module.initialize_rag_manager(embedding_model)
                logger.info(
                    f"RAG manager initialized: {initialized_manager is not None}"
                )
            except Exception as e:
                logger.error(f"Failed to initialize RAG manager: {e}")
                raise

        # Create RAG session
        session_id = rag_module.rag_manager.create_session(rag_chunks)

        # Create sample data from chunks (first few chunks)
        sample_data = [
            {"chunk": chunk[:200] + "..." if len(chunk) > 200 else chunk}
            for chunk in rag_chunks[:5]
        ]

        response = {
            "filename": file.filename,
            "file_type": file_type,
            "num_rows": 0,  # Will be determined by document loader
            "num_columns": 0,  # Will be determined by document loader
            "columns": [],  # Will be determined by document loader
            "sample_data": sample_data,
            "session_id": session_id,
            "chunks_count": len(rag_chunks),
        }

        logger.info(
            f"Processed file {file.filename} into {len(rag_chunks)} chunks, created session {session_id}"
        )
        return response

    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/query", response_model=drilling_schema.QueryResponse)
def query_drilling_data(query: drilling_schema.QueryRequest):
    try:
        # Initialize RAG manager if not already done
        if rag_module.rag_manager is None:
            logger.info("Initializing RAG manager for first use")
            embedding_model = get_embedding_model()
            rag_module.initialize_rag_manager(embedding_model)

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
    # Initialize RAG manager if not already done
    if rag_module.rag_manager is None:
        logger.info("Initializing RAG manager for first use")
        embedding_model = get_embedding_model()
        rag_module.initialize_rag_manager(embedding_model)

    session_info = rag_module.rag_manager.get_session_info(session_id)
    if session_info is None:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    return session_info
