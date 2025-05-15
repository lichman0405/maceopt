# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/main.py

from fastapi import FastAPI
from app.api import router as optimize_router
from app.utils import logger

app = FastAPI(
    title="MACEOPT Geometry Optimization API",
    description="Optimize atomic structures using MACE + ASE + BFGS.",
    version="0.1.0"
)

# Register API routes
app.include_router(optimize_router, prefix="")

# Lifecycle hooks
@app.on_event("startup")
async def startup_event():
    logger.print("[bold green]🚀 MACEOPT API starting up...[/]")

@app.on_event("shutdown")
async def shutdown_event():
    logger.print("[bold red]🛑 MACEOPT API shutting down...[/]")
