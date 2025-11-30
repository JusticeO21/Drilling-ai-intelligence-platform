from fastapi import FastAPI
from services.api.app.routers import drilling, chat
from common.config import settings
from common.chroma_client import get_chroma_client as init_chroma_client
from common.redis_client import get_redis_client as init_redis_client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version=settings.version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drilling.router, prefix="/drilling", tags=["drilling"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    init_chroma_client()
    init_redis_client()


@app.get("/")
async def root():
    return {"message": "Welcome to Oil Drilling Dashboard API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
