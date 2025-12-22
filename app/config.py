# The module is to configure default paths and settings for the application.
# Author: Shibo Li
# Date: 2025-12-22
# Version: 0.3.1

import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Model Configuration
    mace_model_path: Path = Path("models/mace_agnesi_medium.model")
    
    # Output Directory
    output_dir: Path = Path("output")
    
    # Logging Configuration
    log_dir: Path = Path("logs")
    log_level: str = "INFO"
    log_max_bytes: int = 10 * 1024 * 1024  # 10MB
    log_backup_count: int = 5
    
    # Server Configuration
    uvicorn_host: str = "0.0.0.0"
    uvicorn_port: int = 4748
    workers: int = 4
    
    # File Upload Limits (in MB)
    max_upload_size_mb: int = 50
    
    # Supported file formats
    supported_formats: List[str] = [".xyz", ".cif", ".vasp", ".poscar", ".contcar"]
    
    # Device Configuration
    # Options: auto, cpu, cuda, mps
    device: str = "auto"
    
    # Structure validation
    max_atoms_warning: int = 1000  # Warn for large structures
    max_atoms_limit: int = 10000   # Hard limit
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def max_upload_size_bytes(self) -> int:
        """Convert MB to bytes"""
        return self.max_upload_size_mb * 1024 * 1024


# Create global settings instance
settings = Settings()

# Backwards compatibility - keep old variable names
DEFAULT_MODEL_PATH = settings.mace_model_path
DEFAULT_OUTPUT_DIR = settings.output_dir
UVICORN_HOST = settings.uvicorn_host
UVICORN_PORT = settings.uvicorn_port
WORKERS = settings.workers
MAX_UPLOAD_SIZE_MB = settings.max_upload_size_mb
MAX_UPLOAD_SIZE_BYTES = settings.max_upload_size_bytes
DEVICE = settings.device
