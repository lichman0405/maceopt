# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/core.py

from pathlib import Path
from typing import Dict, Tuple

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
        output_dir: Path,
        fmax: float = 0.1
    ) -> Dict:
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

        # 输出路径
        output_xyz = output_dir / "optimized.xyz"
        output_extxyz = output_dir / "optimized.extxyz"

        # 写入两个文件：标准xyz与extxyz
        write(str(output_xyz), atoms, format="xyz")
        write(str(output_extxyz), atoms, format="extxyz")
        logger.success(f"Optimized structure written to:\n  ├─ {output_xyz}\n  └─ {output_extxyz}")

        # 提取结构信息
        energy = atoms.get_potential_energy()
        free_energy = atoms.info.get("free_energy", energy)
        stress = atoms.get_stress().tolist()
        pbc = atoms.get_pbc().tolist()

        properties = {
            key: f"{arr.dtype.kind.upper()}:{arr.shape[1]}" if arr.ndim == 2 else f"{arr.dtype.kind.upper()}:1"
            for key, arr in atoms.arrays.items()
        }

        return {
            "success": True,
            "n_atoms": len(atoms),
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
