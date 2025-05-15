# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/core/core.py

from pathlib import Path
from typing import Dict

from ase.io import read, write
from ase.optimize import BFGS
from mace.calculators import MACECalculator

from app.utils import logger


class GeometryOptimizer:
    def __init__(self, model_path: Path, device: str = "cpu"):
        self.model_path = model_path
        self.device = device

        if not self.model_path.exists():
            logger.error(f"[maceopt] MACE model not found: {self.model_path}")
            raise FileNotFoundError(f"MACE model not found: {self.model_path}")

        logger.info(f"[maceopt] Loading MACE model from: {self.model_path}")
        self.calculator = MACECalculator(
            model_paths=[str(self.model_path)],
            device=self.device
        )

    def optimize(
        self,
        input_file: Path,
        output_file: Path,
        fmax: float = 0.1
    ) -> Dict:
        """
        Run geometry optimization using MACE + ASE + BFGS

        Args:
            input_file (Path): path to input .xyz structure
            output_file (Path): path to save optimized .xyz
            fmax (float): convergence threshold (eV/Å)

        Returns:
            Dict: summary of optimization
        """
        if not input_file.exists():
            logger.error(f"[maceopt] Input file not found: {input_file}")
            raise FileNotFoundError(f"Input file not found: {input_file}")

        logger.info(f"[maceopt] Reading input structure: {input_file}")
        atoms = read(str(input_file))
        logger.info(f"[maceopt] Number of atoms: {len(atoms)}")

        atoms.set_calculator(self.calculator)

        logger.info(f"[maceopt] Starting BFGS optimization (fmax = {fmax})...")
        optimizer = BFGS(atoms, logfile=None)
        optimizer.run(fmax=fmax)
        logger.info(f"[maceopt] Optimization complete.")

        output_file.parent.mkdir(parents=True, exist_ok=True)
        write(str(output_file), atoms)
        logger.info(f"[maceopt] Optimized structure saved to: {output_file}")

        return {
            "success": True,
            "n_atoms": len(atoms),
            "input_file": str(input_file),
            "output_file": str(output_file),
            "fmax": fmax,
            "device": self.device
        }
