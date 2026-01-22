"""Main Application"""

from fastapi import FastAPI

from .interfaces.api.routes.user import router as credit_decisions_router

app = FastAPI(
    title="Credit Engine API",
    description="Motor de Decisão de Crédito",
    version="0.1.0",
)

app.include_router(credit_decisions_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Template KDB", "version": "0.0.0"}
