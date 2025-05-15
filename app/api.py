# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/api.py

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pathlib import Path

from app.parser import parse_optimization_request
from app.core import GeometryOptimizer
from app.utils import logger
from app.config import DEFAULT_MODEL_PATH, DEFAULT_OUTPUT_DIR


from fastapi.responses import FileResponse
from fastapi import Query, HTTPException
from app.config import DEFAULT_OUTPUT_DIR

router = APIRouter()

# API route for optimization
@router.post("/optimize")
async def optimize_route(
    structure_file: UploadFile = File(...),
    fmax: float = Form(0.1),
    device: str = Form("cpu")
):
    logger.rule("[bold blue]API - Optimization Request Received")

    # Parse and validate input
    opt_req = parse_optimization_request(structure_file, fmax, device)

    # Construct output path
    output_file = DEFAULT_OUTPUT_DIR / f"{Path(opt_req.original_filename).stem}_opt.xyz"

    # Run optimization
    optimizer = GeometryOptimizer(model_path=DEFAULT_MODEL_PATH, device=opt_req.params.device)
    result = optimizer.optimize(
        input_file=opt_req.input_path,
        output_file=output_file,
        fmax=opt_req.params.fmax
    )

    logger.success("Optimization complete. Returning response.")
    return JSONResponse(content=result)

# API route for downloading optimized structure
@router.get("/download")
async def download_structure(filename: str = Query(..., description="Optimized XYZ filename")):
    logger.rule(f"[bold blue]API - Download Request: {filename}")
    
    file_path = DEFAULT_OUTPUT_DIR / filename

    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail="File not found.")

    logger.success(f"Serving file: {file_path}")
    return FileResponse(path=file_path, filename=filename, media_type="chemical/x-xyz")
