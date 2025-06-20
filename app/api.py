# The module provides FastAPI endpoints for geometry optimization requests.
# Author: Shibo Li
# Date: 2025-05-15
# Version: 0.2.0


from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path

from app.parser import parse_optimization_request
from app.core import GeometryOptimizer
from app.utils import logger
from app.config import DEFAULT_MODEL_PATH, DEFAULT_OUTPUT_DIR

router = APIRouter()


@router.post("/optimize")
async def optimize_route(
    structure_file: UploadFile = File(...),
    fmax: float = Form(0.1),
    device: str = Form("cpu")
):
    logger.rule("[bold blue]API - Optimization Request Received")


    opt_req = parse_optimization_request(structure_file, fmax, device)

    optimizer = GeometryOptimizer(model_path=DEFAULT_MODEL_PATH, device=opt_req.params.device)
    result = optimizer.optimize(
        input_file=opt_req.original_path,
        output_dir=opt_req.output_dir,
        fmax=opt_req.params.fmax
    )

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
