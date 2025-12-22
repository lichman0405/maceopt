# The module is to configure default paths and settings for the application.
# Author: Shibo Li
# Date: 2025-06-16
# Version: 0.3.0

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Model Configuration
DEFAULT_MODEL_PATH = Path(os.getenv("MACE_MODEL_PATH", "models/mace_agnesi_medium.model"))

# Output Directory
DEFAULT_OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output"))

# Server Configuration
UVICORN_HOST = os.getenv("UVICORN_HOST", "0.0.0.0")
UVICORN_PORT = int(os.getenv("UVICORN_PORT", "4748"))
WORKERS = int(os.getenv("WORKERS", "4"))

# File Upload Limits (in bytes)
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024

# Device Configuration
# Options: auto, cpu, cuda, mps
DEVICE = os.getenv("DEVICE", "auto")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
