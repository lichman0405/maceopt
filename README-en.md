
<div align="center">
  <a href="https://github.com/lichman0405/maceopt.git">
    <img src="assets/edit_logo.png" alt="Logo" width="200px">
  </a>

  <h1 align="center">MACEOPT API Service</h1>

  <p align="center">
    This is a lightweight FastAPI service for geometry optimization of atomic structures (such as MOFs, molecules, materials). It combines the MACE neural force field with the ASE optimizer and supports uploading <code>.cif</code> structure files. The results of each optimization task are automatically saved per session and provide both the optimized <code>.cif</code> (standard structure) and <code>.extcif</code> (containing energy, forces, stress, etc.) files, with download and tracking supported.
    <br>
    <a href="README.md"><strong>中文</strong></a>
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

---

## 🚀 Features

- Support uploading structure files (`.cif`)
- Uses MACE-MP-0 force field + ASE BFGS optimizer
- Automatically creates a separate session directory for each optimization task
- Optimization output includes:
  - `optimized.cif` (standard structure file)
  - `optimized.extcif` (with additional physical data: energy, forces, stress, etc.)
- Returns complete physical quantities (energy, stress, periodic boundary conditions, forces, etc.)
- Rich terminal logging (powered by `rich`)
- Supports one-click deployment with Docker

---

## 📦 Installation

```bash
git clone https://github.com/lichman0405/maceopt.git
cd maceopt
pip install -r requirements.txt
```

---

## 🧪 Run Locally

```bash
uvicorn app.main:app --reload --port 4748
```

Open [http://localhost:4748/docs](http://localhost:4748/docs) to access the Swagger UI test page.

---

## 🔁 API Endpoints

### ✅ POST `/optimize`

This endpoint accepts a structure file and performs geometry optimization using the MACE force field.

**Request Body:**

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `structure_file` | file | ✅ | - | Structure file (`.cif`) to optimize. |
| `fmax` | float | ❌ | `0.1` | Convergence threshold, meaning the maximum force on any atom. |
| `steps` | int | ❌ | `100` | Maximum number of optimization steps. |
| `optimizer_name` | string | ❌ | `BFGS` | ASE optimizer to use. |
| `device` | string | ❌ | `cpu` | Device to run MACE model (`cpu` or `cuda`). |

**Response Body (on success):**

```json
{
  "session_id": "string",
  "message": "Optimization successful",
  "optimized_structure_cif": "string",
  "optimized_structure_extcif": "string",
  "download_link_cif": "/download/{session_id}/optimized.cif",
  "download_link_extcif": "/download/{session_id}/optimized.extcif",
  "log_output": "string"
}
```

- **`session_id`**: Unique ID for the optimization task.
- **`message`**: Status message.
- **`optimized_structure_cif`**: Content of the optimized `.cif` file.
- **`optimized_structure_extcif`**: Content of the optimized `.extcif` file with extra physical data.
- **`download_link_cif`**: Direct link to download the `.cif` file.
- **`download_link_extcif`**: Direct link to download the `.extcif` file.
- **`log_output`**: Detailed log of the optimization process.

---

## 🐳 Deploy with Docker

### Build Image

```bash
docker build -t maceopt .
```

### Run Service

```bash
docker run -it --rm -p 4748:8000 maceopt
```

Then visit: `http://localhost:4748/docs`

---

## 📁 Project Structure

```
maceopt/
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── api.py           # API routes
│   ├── parser.py        # Argument parsing & session path
│   ├── core.py          # Core optimization logic (MACE + ASE)
│   ├── utils.py         # Rich logging utility
│   └── config.py        # Default model & path configs
├── models/              # MACE pretrained models
├── examples/            # Example input structures
├── output/              # Auto-generated session directories
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 📚 References

This project is based on the following models and tools:

- Batzner et al., *E(3)-equivariant Graph Neural Networks for Data-Efficient and Accurate Interatomic Potentials*, Nature Communications, 2022
- [MACE Model](https://github.com/ACEsuit/mace)
- [ASE Optimizer](https://wiki.fysik.dtu.dk/ase/)

---

## 👤 Author

Li Shibo · 2025  
MIT License
