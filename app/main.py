# The module provides FastAPI endpoints for geometry optimization requests.
# Author: Shibo Li
# Date: 2025-12-22
# Version: 0.3.1


from fastapi import FastAPI
from app.api import router as optimize_router
from app.utils import logger
from app.config import settings

app = FastAPI(
    title="MACEOPT Geometry Optimization API",
    description="Optimize atomic structures using MACE + ASE + BFGS with automatic GPU detection and multi-format support.",
    version="0.3.1"
)

app.include_router(optimize_router, prefix="")

@app.on_event("startup")
async def startup_event():
    # Ensure directories exist
    settings.output_dir.mkdir(parents=True, exist_ok=True)
    settings.log_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("[bold green]🚀 MACEOPT API starting up...[/]")
    logger.info(f"[bold green]📁 Output directory:[/] {settings.output_dir}")
    logger.info(f"[bold green]📝 Log directory:[/] {settings.log_dir}")
    logger.info(f"[bold green]⚙️  Device:[/] {settings.device}")
    logger.info(f"[bold green]📋 Supported formats:[/] {', '.join(settings.supported_formats)}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("[bold red]🛑 MACEOPT API shutting down...[/]")
