# The module provides a parser for geometry optimization requests.
# Author: Shibo Li
# Date: 2025-05-15
# Version: 0.2.0

import uuid
from pathlib import Path
from dataclasses import dataclass
from fastapi import UploadFile, File, Form, HTTPException
from pydantic import BaseModel, Field

from app.utils import logger
from app.config import DEFAULT_OUTPUT_DIR


class OptimizeParams(BaseModel):
    fmax: float = Field(0.1, gt=0.0, description="Convergence threshold in eV/Å")
    device: str = Field("cpu", description="Device to use: 'cpu' or 'cuda'")


@dataclass
class OptimizationRequest:
    original_path: Path
    session_id: str
    output_dir: Path
    params: OptimizeParams


def parse_optimization_request(
    structure_file: UploadFile = File(...),
    fmax: float = Form(0.1),
    device: str = Form("cpu")
) -> OptimizationRequest:
    filename = structure_file.filename
    if filename is None:
        raise HTTPException(status_code=400, detail="Uploaded file must have a filename")
    suffix = Path(filename).suffix.lower()

    logger.rule("[bold blue]Parsing structure upload")
    logger.info(f"[cyan]- Uploaded file:[/] {filename}")

    if suffix != ".xyz":
        raise HTTPException(status_code=400, detail="Only .xyz files are supported")

    session_id = f"session_{uuid.uuid4().hex[:8]}"
    output_dir = DEFAULT_OUTPUT_DIR / session_id
    output_dir.mkdir(parents=True, exist_ok=True)

    original_path = output_dir / "original.xyz"
    with original_path.open("wb") as f:
        content = structure_file.file.read()
        f.write(content)

    logger.info(f"[green]- Saved to:[/] {original_path}")
    logger.info(f"[magenta]- Session:[/] {session_id}")

    return OptimizationRequest(
        original_path=original_path,
        session_id=session_id,
        output_dir=output_dir,
        params=OptimizeParams(fmax=fmax, device=device)
    )
