# The module provides a class for geometry optimization using the MACE calculator.
# Author: Shibo Li
# Date: 2025-06-16
# Version: 0.3.0

import torch
from pathlib import Path
from typing import Dict, Optional

from ase.io import read, write
from ase.optimize import BFGS
from mace.calculators import MACECalculator

from app.utils import logger


def detect_device(device: str = "auto") -> str:
    """
    Automatically detect the best available device for computation.
    
    Args:
        device: Device preference (auto/cpu/cuda/mps)
        
    Returns:
        str: The device to use (cpu/cuda/mps)
    """
    if device.lower() != "auto":
        # User specified device, validate and return
        device_lower = device.lower()
        if device_lower == "cuda" and not torch.cuda.is_available():
            logger.warning(f"CUDA requested but not available, falling back to CPU")
            return "cpu"
        if device_lower == "mps" and not (hasattr(torch.backends, "mps") and torch.backends.mps.is_available()):
            logger.warning(f"MPS requested but not available, falling back to CPU")
            return "cpu"
        return device_lower
    
    # Auto detection
    try:
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            logger.info(f"[bold green]✔ GPU Detected:[/] {device_name}")
            return "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            logger.info(f"[bold green]✔ MPS Detected:[/] Apple Silicon GPU")
            return "mps"
        else:
            logger.info(f"[bold yellow]⚠ No GPU detected, using CPU[/]")
            return "cpu"
    except Exception as e:
        logger.warning(f"Error detecting device: {e}, falling back to CPU")
        return "cpu"


class GeometryOptimizer:
    """
    Geometry optimizer using MACE calculator and ASE BFGS optimizer.
    
    Args:
        model_path: Path to the MACE model file
        device: Device to use (auto/cpu/cuda/mps)
    """
    
    def __init__(self, model_path: Path, device: str = "auto"):
        self.model_path = model_path
        self.device = detect_device(device)

        if not self.model_path.exists():
            error_msg = f"MACE model not found: {self.model_path}"
            logger.error(f"[maceopt] {error_msg}")
            raise FileNotFoundError(error_msg)

        logger.info(f"[maceopt] Loading MACE model from: {self.model_path}")
        logger.info(f"[maceopt] Using device: [bold cyan]{self.device.upper()}[/]")
        
        try:
            self.calculator = MACECalculator(
                model_paths=[str(self.model_path)],
                device=self.device
            )
            logger.success(f"[maceopt] MACE calculator initialized successfully")
        except Exception as e:
            error_msg = f"Failed to initialize MACE calculator: {str(e)}"
            logger.error(f"[maceopt] {error_msg}")
            raise RuntimeError(error_msg) from e

    def optimize(
        self,
        input_file: Path,
        output_dir: Path,
        fmax: float = 0.1,
        max_steps: Optional[int] = None
    ) -> Dict:
        """
        Optimize the geometry of a structure.
        
        Args:
            input_file: Path to input structure file
            output_dir: Directory to save output files
            fmax: Force convergence threshold (eV/Å)
            max_steps: Maximum optimization steps (None = unlimited)
            
        Returns:
            Dict containing optimization results and metadata
        """
        if not input_file.exists():
            error_msg = f"Input file not found: {input_file}"
            logger.error(f"[maceopt] {error_msg}")
            raise FileNotFoundError(error_msg)

        logger.info(f"[maceopt] Reading input structure: {input_file}")
        
        try:
            atoms = read(str(input_file))
        except Exception as e:
            error_msg = f"Failed to read input file: {str(e)}"
            logger.error(f"[maceopt] {error_msg}")
            raise ValueError(error_msg) from e

        if isinstance(atoms, list):
            logger.info(f"[maceopt] Multiple structures found, using the first one.")
            atoms = atoms[0]
        
        n_atoms = len(atoms)
        logger.info(f"[maceopt] Number of atoms: {n_atoms}")

        try:
            atoms.set_calculator(self.calculator)
        except Exception as e:
            error_msg = f"Failed to set calculator: {str(e)}"
            logger.error(f"[maceopt] {error_msg}")
            raise RuntimeError(error_msg) from e

        logger.info(f"[maceopt] Starting BFGS optimization (fmax = {fmax})...")
        
        try:
            optimizer = BFGS(atoms, logfile=None)
            if max_steps:
                optimizer.run(fmax=fmax, steps=max_steps)
                logger.info(f"[maceopt] Optimization complete (max_steps={max_steps}).")
            else:
                optimizer.run(fmax=fmax)
                logger.info(f"[maceopt] Optimization converged.")
        except Exception as e:
            error_msg = f"Optimization failed: {str(e)}"
            logger.error(f"[maceopt] {error_msg}")
            raise RuntimeError(error_msg) from e

        # Save output files
        output_xyz = output_dir / "optimized.xyz"
        output_extxyz = output_dir / "optimized.extxyz"

        try:
            write(str(output_xyz), atoms, format="xyz")
            write(str(output_extxyz), atoms, format="extxyz")
            logger.success(f"Optimized structure written to:\n  ├─ {output_xyz}\n  └─ {output_extxyz}")
        except Exception as e:
            error_msg = f"Failed to write output files: {str(e)}"
            logger.error(f"[maceopt] {error_msg}")
            raise IOError(error_msg) from e

        # Extract results
        try:
            energy = atoms.get_potential_energy()
            free_energy = atoms.info.get("free_energy", energy)
            stress = atoms.get_stress().tolist()
            pbc = atoms.get_pbc().tolist()

            properties = {
                key: f"{arr.dtype.kind.upper()}:{arr.shape[1]}" if arr.ndim == 2 else f"{arr.dtype.kind.upper()}:1"
                for key, arr in atoms.arrays.items()
            }
        except Exception as e:
            error_msg = f"Failed to extract results: {str(e)}"
            logger.error(f"[maceopt] {error_msg}")
            raise RuntimeError(error_msg) from e

        return {
            "success": True,
            "n_atoms": n_atoms,
            "input_file": str(input_file),
            "output_file": str(output_xyz),
            "output_extxyz": str(output_extxyz),
            "fmax": fmax,
            "device": self.device,
            "energy": energy,
            "free_energy": free_energy,
            "stress": stress,
            "pbc": pbc,
            "properties": properties
        }
