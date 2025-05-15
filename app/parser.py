# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/parser.py

from fastapi import UploadFile, File, Form, HTTPException
from pydantic import BaseModel, Field
from dataclasses import dataclass
from pathlib import Path
import tempfile
import shutil
import hashlib

from app.utils import logger


ALLOWED_EXTENSIONS = {".xyz"}


class OptimizeParams(BaseModel):
    fmax: float = Field(0.1, gt=0.0, description="Convergence threshold in eV/Å")
    device: str = Field("cpu", description="Device to use: 'cpu' or 'cuda'")


@dataclass
class OptimizationRequest:
    input_path: Path
    params: OptimizeParams
    original_filename: str
    file_hash: str


def parse_optimization_request(
    structure_file: UploadFile = File(...),
    fmax: float = Form(0.1),
    device: str = Form("cpu")
) -> OptimizationRequest:
    """
    Validate and save uploaded structure file, return parsed params and metadata.
    """
    filename = structure_file.filename
    suffix = Path(filename).suffix.lower()

    logger.print(f"[blue][parser] Received structure file:[/] {filename}")

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")

    # Compute file hash (for future caching use)
    content = structure_file.file.read()
    file_hash = hashlib.sha256(content).hexdigest()
    structure_file.file.seek(0)  # reset file cursor

    # Save file to a temp path with proper suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(structure_file.file, tmp)
        input_path = Path(tmp.name)

    logger.print(f"[green][parser] Structure saved to:[/] {input_path}")
    logger.print(f"[cyan][parser] SHA256 hash:[/] {file_hash}")

    params = OptimizeParams(fmax=fmax, device=device)
    logger.print(f"[cyan][parser] Parsed params:[/] fmax={params.fmax}, device={params.device}")

    return OptimizationRequest(
        input_path=input_path,
        params=params,
        original_filename=filename,
        file_hash=file_hash
    )
