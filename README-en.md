
<div align="center">
  <a href="https://github.com/lichman0405/maceopt.git">
    <img src="assets/edit_logo.png" alt="Logo" width="200px">
  </a>

  <h1 align="center">MACEOPT API Service</h1>

  <p align="center">
    MACEOPT is a lightweight FastAPI-based service for geometry optimization of atomic structures such as MOFs, molecules, and materials. 
    <br>
    <a href="./README.md"><strong>中文</strong></a>
    ·
    <a href="https://github.com/lichman0405/maceopt.git/issues">Report Bug</a>
    ·
    <a href="https://github.com/lichman0405/maceopt.git/issues">Request Feature</a>
  </p>
</div>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker)
[![GitHub issues](https://img.shields.io/github/issues/lichman0405/maceopt.svg)](https://github.com/lichman0405/maceopt/issues)
[![GitHub stars](https://img.shields.io/github/stars/lichman0405/maceopt.svg?style=social)](https://github.com/lichman0405/maceopt.git)

</div>


## 📌 Overview

**MACEOPT** is a lightweight FastAPI-based service for geometry optimization of atomic structures such as MOFs, molecules, and materials.  
It combines the MACE neural force field with the ASE optimizer. You can upload `.xyz` files, and the system will automatically save the session outputs (`.xyz` and `.extxyz`) with download and tracking support.

## ✨ Features

- Upload `.xyz` structure files
- Uses MACE-MP-0 force field + ASE BFGS optimizer
- Automatically creates session directories for each task
- Outputs include:
  - `optimized.xyz` (standard structure)
  - `optimized.extxyz` (includes energy, forces, stress, etc.)
- Returns complete physical quantities (energy, stress, PBC, forces, etc.)
- Rich terminal logs (using rich)
- One-click Docker deployment

## ⚙️ Installation

```bash
git clone https://github.com/your-org/maceopt.git
cd maceopt
pip install -r requirements.txt
```

## 🚀 Run Locally

```bash
uvicorn app.main:app --reload --port 4748
```

Open [http://localhost:4748/docs](http://localhost:4748/docs) to access the Swagger UI.

## 📡 API Endpoints

### ✅ POST `/optimize`

| Parameter       | Type   | Required | Example     |
|-----------------|--------|----------|-------------|
| structure_file  | file   | ✅        | `test.xyz`  |
| fmax            | float  | ❌        | `0.1`       |
| device          | string | ❌        | `cpu`       |

**Sample Response:**

```json
{
  "success": true,
  "n_atoms": 3,
  "input_file": "...",
  "output_file": ".../optimized.xyz",
  "output_extxyz": ".../optimized.extxyz",
  "energy": -14.26,
  "stress": [...],
  "pbc": [false, false, false],
  "properties": { ... },
  "download_links": {
    "xyz": "/download?path=.../optimized.xyz",
    "extxyz": "/download?path=.../optimized.extxyz"
  }
}
```

### ⬇️ GET `/download`

Use the `download_links` in the response to download:

```bash
curl -O "http://localhost:4748/download?path=session_xxx/optimized.xyz"
curl -O "http://localhost:4748/download?path=session_xxx/optimized.extxyz"
```

## 🐳 Docker Deployment

### Build the Image

```bash
docker build -t maceopt .
```

### Run the Container

```bash
docker run -it --rm -p 4748:8000 maceopt
```

Access [http://localhost:4748/docs](http://localhost:4748/docs)

## 📂 Project Structure

```
maceopt/
├── app/               # FastAPI app and core logic
├── models/            # MACE trained models
├── examples/          # Example input structures
├── output/            # Optimization output
├── requirements.txt
├── Dockerfile
└── README.md
```

## 📖 References

- Batzner et al., *Nature Communications* (2022)
- [MACE](https://github.com/ACEsuit/mace)
- [ASE](https://wiki.fysik.dtu.dk/ase/)

## 👤 Author

Li Shibo · 2025  
MIT License