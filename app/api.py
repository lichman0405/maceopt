# The module provides FastAPI endpoints for geometry optimization requests.
# Author: Shibo Li
# Date: 2025-05-15
# Version: 0.3.0

import torch
from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path

from app.parser import parse_optimization_request
from app.core import GeometryOptimizer, detect_device
from app.utils import logger
from app.config import (
    DEFAULT_MODEL_PATH, 
    DEFAULT_OUTPUT_DIR, 
    MAX_UPLOAD_SIZE_BYTES,
    MAX_UPLOAD_SIZE_MB,
    DEVICE
)

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    """
    return {
        "status": "healthy",
        "service": "maceopt",
        "version": "0.3.0"
    }


@router.get("/info")
async def server_info():
    """
    Get server information including GPU availability.
    """
    device = detect_device(DEVICE)
    
    info = {
        "service": "MACEOPT Geometry Optimization API",
        "version": "0.3.0",
        "model_path": str(DEFAULT_MODEL_PATH),
        "device": device.upper(),
        "max_upload_size_mb": MAX_UPLOAD_SIZE_MB,
        "supported_formats": [".xyz"]
    }
    
    # Add GPU info if available
    if device == "cuda" and torch.cuda.is_available():
        info["gpu_info"] = {
            "name": torch.cuda.get_device_name(0),
            "memory_total_gb": round(torch.cuda.get_device_properties(0).total_memory / 1024**3, 2),
            "cuda_version": torch.version.cuda
        }
    elif device == "mps":
        info["gpu_info"] = {
            "name": "Apple Silicon GPU",
            "backend": "MPS"
        }
    
    return info


@router.post("/optimize")
async def optimize_route(
    structure_file: UploadFile = File(...),
    fmax: float = Form(0.1),
    device: str = Form("auto")
):
    """
    Optimize atomic structure geometry.
    
    Args:
        structure_file: .xyz structure file
        fmax: Force convergence threshold (eV/Å)
        device: Device to use (auto/cpu/cuda/mps)
        
    Returns:
        JSON with optimization results and download links
    """
    logger.rule("[bold blue]API - Optimization Request Received")

    # Validate file size
    try:
        contents = await structure_file.read()
        file_size = len(contents)
        
        if file_size > MAX_UPLOAD_SIZE_BYTES:
            logger.error(f"❌ File too large: {file_size / 1024**2:.2f} MB (max: {MAX_UPLOAD_SIZE_MB} MB)")
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds maximum allowed size of {MAX_UPLOAD_SIZE_MB} MB"
            )
        
        # Reset file pointer for parser
        await structure_file.seek(0)
        logger.info(f"[cyan]- File size:[/] {file_size / 1024:.2f} KB")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to read uploaded file: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to read uploaded file: {str(e)}")

    # Parse request
    try:
        opt_req = parse_optimization_request(structure_file, fmax, device)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to parse request: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to parse request: {str(e)}")

    # Run optimization
    try:
        optimizer = GeometryOptimizer(
            model_path=DEFAULT_MODEL_PATH, 
            device=opt_req.params.device
        )
        result = optimizer.optimize(
            input_file=opt_req.original_path,
            output_dir=opt_req.output_dir,
            fmax=opt_req.params.fmax
        )
    except FileNotFoundError as e:
        logger.error(f"❌ Model or input file not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        logger.error(f"❌ Invalid input: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        logger.error(f"❌ Optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    # Add download links
    session_rel = opt_req.output_dir.relative_to(DEFAULT_OUTPUT_DIR)
    result["session"] = str(session_rel)
    result["download_links"] = {
        "xyz": f"/download?path={session_rel}/optimized.xyz",
        "extxyz": f"/download?path={session_rel}/optimized.extxyz"
    }

    logger.success("Optimization complete. Returning full metadata.")
    return JSONResponse(content=result)


@router.get("/download")
async def download_structure(path: str = Query(..., description="Path relative to output/ directory")):
    logger.rule(f"[bold blue]API - Download Request: {path}")

    full_path = Path("output") / path
    full_path = full_path.resolve()

    output_root = DEFAULT_OUTPUT_DIR.resolve()
    if not str(full_path).startswith(str(output_root)):
        logger.error("❌ Unsafe path access attempt")
        raise HTTPException(status_code=400, detail="Invalid path.")

    if not full_path.exists():
        logger.error(f"❌ File not found: {full_path}")
        raise HTTPException(status_code=404, detail="File not found.")

    logger.success(f"✅ Serving file: {full_path}")
    return FileResponse(
        path=full_path,
        filename=full_path.name,
        media_type="application/octet-stream"
    )
