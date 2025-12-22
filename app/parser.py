# The module provides a parser for geometry optimization requests.
# Author: Shibo Li
# Date: 2025-12-22
# Version: 0.3.1

import uuid
from pathlib import Path
from dataclasses import dataclass
from fastapi import UploadFile, File, Form
from pydantic import BaseModel, Field

from app.utils import logger
from app.config import settings
from app.errors import FileError, ErrorCode


class OptimizeParams(BaseModel):
    fmax: float = Field(0.1, gt=0.0, description="Convergence threshold in eV/Å")
    device: str = Field("auto", description="Device to use: 'cpu', 'cuda', 'mps', or 'auto'")


@dataclass
class OptimizationRequest:
    original_path: Path
    session_id: str
    output_dir: Path
    params: OptimizeParams


# Format descriptions
FORMAT_DESCRIPTIONS = {
    '.xyz': 'XYZ coordinate file (standard format)',
    '.cif': 'Crystallographic Information File (recommended for MOF/crystals)',
    '.vasp': 'VASP POSCAR/CONTCAR format',
    '.poscar': 'VASP POSCAR format',
    '.contcar': 'VASP CONTCAR format',
}


def parse_optimization_request(
    structure_file: UploadFile = File(...),
    fmax: float = Form(0.1),
    device: str = Form("auto")
) -> OptimizationRequest:
    filename = structure_file.filename
    if filename is None:
        raise FileError(
            ErrorCode.MISSING_REQUIRED_FIELD,
            "Uploaded file must have a filename"
        )
    
    suffix = Path(filename).suffix.lower()

    logger.rule("[bold blue]Parsing structure upload")
    logger.info(f"[cyan]- Uploaded file:[/] {filename}")

    # Validate file format
    if suffix not in settings.supported_formats:
        supported_list = ", ".join(settings.supported_formats)
        raise FileError(
            ErrorCode.FILE_INVALID_FORMAT,
            f"Unsupported file format: {suffix}",
            {
                "uploaded_format": suffix,
                "supported_formats": settings.supported_formats,
                "suggestion": f"Please upload one of: {supported_list}"
            }
        )
    
    # Log format info
    format_desc = FORMAT_DESCRIPTIONS.get(suffix, "Unknown format")
    logger.info(f"[green]- Format:[/] {format_desc}")

    session_id = f"session_{uuid.uuid4().hex[:8]}"
    output_dir = settings.output_dir / session_id
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save with original extension
    original_filename = f"original{suffix}"
    original_path = output_dir / original_filename
    
    try:
        with original_path.open("wb") as f:
            content = structure_file.file.read()
            f.write(content)
    except Exception as e:
        raise FileError(
            ErrorCode.FILE_READ_FAILED,
            f"Failed to save uploaded file: {str(e)}"
        )

    logger.info(f"[green]- Saved to:[/] {original_path}")
    logger.info(f"[magenta]- Session:[/] {session_id}")

    return OptimizationRequest(
        original_path=original_path,
        session_id=session_id,
        output_dir=output_dir,
        params=OptimizeParams(fmax=fmax, device=device)
    )
