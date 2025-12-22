# The module provides FastAPI endpoints for geometry optimization requests.
# Author: Shibo Li
# Date: 2025-06-16
# Version: 0.3.0


from fastapi import FastAPI
from app.api import router as optimize_router
from app.utils import logger
from app.config import DEFAULT_OUTPUT_DIR

app = FastAPI(
    title="MACEOPT Geometry Optimization API",
    description="Optimize atomic structures using MACE + ASE + BFGS with automatic GPU detection.",
    version="0.3.0"
)

app.include_router(optimize_router, prefix="")

@app.on_event("startup")
async def startup_event():
    # Ensure output directory exists
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("[bold green]🚀 MACEOPT API starting up...[/]")
    logger.info(f"[bold green]📁 Output directory:[/] {DEFAULT_OUTPUT_DIR}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("[bold red]🛑 MACEOPT API shutting down...[/]")
