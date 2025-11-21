from fastapi import FastAPI
from .routers import wells, drilling, chat
from common.config import settings
from common.logging import logger
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

app.include_router(wells.router, prefix="/wells", tags=["wells"])
app.include_router(drilling.router, prefix="/drilling", tags=["drilling"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])


@app.get("/")
async def root():
    return {"message": "Welcome to Oil Drilling Dashboard API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
