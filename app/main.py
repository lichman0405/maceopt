# The module provides FastAPI endpoints for geometry optimization requests.
# Author: Shibo Li
# Date: 2025-06-16
# Version: 0.2.0


from fastapi import FastAPI
from app.api import router as optimize_router
from app.utils import logger

app = FastAPI(
    title="MACEOPT Geometry Optimization API",
    description="Optimize atomic structures using MACE + ASE + BFGS.",
    version="0.1.0"
)

app.include_router(optimize_router, prefix="")

@app.on_event("startup")
async def startup_event():
    logger.info("[bold green]🚀 MACEOPT API starting up...[/]")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("[bold red]🛑 MACEOPT API shutting down...[/]")
