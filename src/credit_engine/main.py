"""Main Application"""
from fastapi import FastAPI

from .infrastructure.database.init_db import init_db
from .interfaces.api.routes.credit_decisions import router as credit_decisions_router

app = FastAPI(
    title="Credit Engine API",
    description="Motor de Decisão de Crédito",
    version="0.1.0",
)

app.include_router(credit_decisions_router)


@app.on_event("startup")
async def startup_event():
    """Inicializa o banco de dados com dados padrão na inicialização"""
    init_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Credit Engine API", "version": "0.1.0"}
