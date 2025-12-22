# Error code definitions and custom exceptions for MACEOPT API
# Author: Shibo Li
# Date: 2025-12-22
# Version: 0.3.1

from enum import Enum
from typing import Optional, Dict, Any
from fastapi import HTTPException


class ErrorCode(str, Enum):
    """Standard error codes for MACEOPT API"""
    
    # Model errors (MACE_0xx)
    MODEL_NOT_FOUND = "MACE_001"
    MODEL_LOAD_FAILED = "MACE_002"
    
    # File errors (MACE_1xx)
    FILE_TOO_LARGE = "MACE_101"
    FILE_INVALID_FORMAT = "MACE_102"
    FILE_READ_FAILED = "MACE_103"
    FILE_NOT_FOUND = "MACE_104"
    
    # Structure errors (MACE_2xx)
    STRUCTURE_INVALID = "MACE_201"
    STRUCTURE_TOO_LARGE = "MACE_202"
    UNSUPPORTED_ELEMENTS = "MACE_203"
    
    # Optimization errors (MACE_3xx)
    OPTIMIZATION_FAILED = "MACE_301"
    OPTIMIZATION_TIMEOUT = "MACE_302"
    CALCULATOR_ERROR = "MACE_303"
    
    # Request errors (MACE_4xx)
    INVALID_PARAMETERS = "MACE_401"
    MISSING_REQUIRED_FIELD = "MACE_402"
    
    # System errors (MACE_5xx)
    INTERNAL_ERROR = "MACE_501"
    GPU_ERROR = "MACE_502"
    IO_ERROR = "MACE_503"


class MACEException(HTTPException):
    """Base exception for MACEOPT with error code support"""
    
    def __init__(
        self,
        status_code: int,
        error_code: ErrorCode,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        self.error_code = error_code
        self.message = message
        self.details = details or {}
        
        super().__init__(
            status_code=status_code,
            detail={
                "error": {
                    "code": error_code.value,
                    "message": message,
                    "details": self.details
                }
            }
        )


class ModelError(MACEException):
    """Model-related errors"""
    def __init__(self, error_code: ErrorCode, message: str, details: Optional[Dict] = None):
        super().__init__(404, error_code, message, details)


class FileError(MACEException):
    """File-related errors"""
    def __init__(self, error_code: ErrorCode, message: str, details: Optional[Dict] = None):
        super().__init__(400, error_code, message, details)


class StructureError(MACEException):
    """Structure validation errors"""
    def __init__(self, error_code: ErrorCode, message: str, details: Optional[Dict] = None):
        super().__init__(400, error_code, message, details)


class OptimizationError(MACEException):
    """Optimization-related errors"""
    def __init__(self, error_code: ErrorCode, message: str, details: Optional[Dict] = None):
        super().__init__(500, error_code, message, details)


class SystemError(MACEException):
    """System-level errors"""
    def __init__(self, error_code: ErrorCode, message: str, details: Optional[Dict] = None):
        super().__init__(500, error_code, message, details)
