
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

- ✅ **Multi-format support**: `.xyz`, `.cif`, `.vasp`, `.poscar`, `.contcar`
- ✅ Uses MACE-MP-0 force field + ASE BFGS optimizer
- ✅ **Automatic GPU Detection** (CUDA/MPS/CPU smart switching)
- ✅ Automatically creates session directories for each task
- ✅ Outputs include:
  - `optimized.xyz` (standard structure)
  - `optimized.extxyz` (includes energy, forces, stress, etc.)
- ✅ Returns complete physical quantities (energy, stress, PBC, forces, etc.)
- ✅ **Persistent logging**: Rotating file logs (app.log + error.log)
- ✅ **Standardized error codes**: MACE_xxx error code system for professional API responses
- ✅ **Type-safe configuration**: Pydantic Settings-based configuration management
- ✅ **Structure size validation**: Prevents resource exhaustion from oversized structures
- ✅ Rich terminal logs (using rich)
- ✅ One-click Docker deployment
- ✅ Environment variable configuration support
- ✅ Health check endpoints
- ✅ Comprehensive exception handling
- ✅ Production-ready Gunicorn deployment

## ⚙️ Installation

```bash
git clone https://github.com/lichman0405/maceopt.git
cd maceopt
pip install -r requirements.txt
```

### Environment Configuration (Optional)

```bash
# Copy configuration template
cp .env.example .env

# Edit .env file to customize settings
# DEVICE=auto          # auto/cpu/cuda/mps - automatic GPU detection
# MAX_UPLOAD_SIZE_MB=50
# WORKERS=4
```

---

## 🚀 Run Locally

### Development Mode (Single Process)

```bash
uvicorn app.main:app --reload --port 4748
```

### Production Mode (Multi-Process, Recommended)

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:4748 \
  --timeout 300
```

Open [http://localhost:4748/docs](http://localhost:4748/docs) to access the Swagger UI.

### Health Check

```bash
# Check service status
curl http://localhost:4748/health

# Get server information (including GPU info)
curl http://localhost:4748/info
```

## 📡 API Endpoints

### ✅ GET `/health` - Health Check

Returns service health status for monitoring and load balancers.

**Sample Response:**
```json
{
  "status": "healthy",
  "service": "maceopt",
  "version": "0.3.1"
}
```

### ✅ GET `/info` - Server Information

Returns server configuration including GPU detection results.

**Sample Response:**
```json
{
  "service": "MACEOPT Geometry Optimization API",
  "version": "0.3.1",
  "model_path": "models/mace_agnesi_medium.model",
  "device": "CUDA",
  "max_upload_size_mb": 50,
  "supported_formats": [".xyz", ".cif", ".vasp", ".poscar", ".contcar"],
  "gpu_info": {
    "name": "NVIDIA GeForce RTX 4090",
    "memory_total_gb": 24.0,
    "cuda_version": "12.1"
  }
}
```

### ✅ POST `/optimize` - Structure Optimization

| Parameter       | Type   | Required | Example     | Description |
|-----------------|--------|----------|-------------|-------------|
| structure_file  | file   | ✅        | `test.xyz`  | Atomic structure file |
| fmax            | float  | ❌        | `0.1`       | Convergence threshold (eV/Å) |
| device          | string | ❌        | `auto`      | `auto`/`cpu`/`cuda`/`mps` |

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

---

## 🧪 Quick Testing

### Basic Test Workflow

```bash
# 1. Start service
uvicorn app.main:app --reload --port 4748

# 2. Health check (new terminal)
curl http://localhost:4748/health

# 3. Check GPU info
curl http://localhost:4748/info

# 4. Test optimization
curl -X POST http://localhost:4748/optimize \
  -F "structure_file=@examples/h2o.xyz" \
  -F "fmax=0.1" \
  -F "device=auto"

# 5. Open Swagger UI in browser
# http://localhost:4748/docs
```

### Expected Results

- ✅ `/health` returns `{"status": "healthy"}`
- ✅ `/info` shows device type (CUDA/CPU)
- ✅ `/optimize` returns optimization results with download links
- ✅ Session folder generated in `output/` directory

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

### Manual Build

```bash
docker build -t maceopt .
```

### Run Container

**CPU Version:**
```bash
docker run -it --rm -p 4748:8000 -v $(pwd)/output:/app/output maceopt
```

**GPU Version (requires nvidia-docker):**
```bash
docker run -it --rm --gpus all \
  -p 4748:8000 \
  -v $(pwd)/output:/app/output \
  -e DEVICE=auto \
  maceopt
```

Access [http://localhost:4748/docs](http://localhost:4748/docs)

## 📂 Project Structure

```
maceopt/
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── api.py           # API routes and endpoints
│   ├── parser.py        # Request parsing + session path construction
│   ├── core.py          # Core optimization logic (MACE + ASE + GPU detection)
│   ├── utils.py         # Rich logging wrapper + file logging
│   ├── config.py        # Pydantic Settings configuration management
│   └── errors.py        # Error code definitions + custom exceptions
├── models/              # MACE trained models
├── examples/            # Example input structures
├── output/              # Auto-generated optimization session directories
├── logs/                # Log files directory (app.log + error.log)
├── .env.example         # Environment variable template
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Docker Compose configuration
└── README.md
```

---

## ⚙️ Configuration

All configuration options can be set via environment variables (`.env` file):

| Variable | Default | Description |
|----------|---------|-------------|
| `MACE_MODEL_PATH` | `models/mace_agnesi_medium.model` | MACE model path |
| `OUTPUT_DIR` | `output` | Output directory |
| `DEVICE` | `auto` | Compute device (auto-detection) |
| `MAX_UPLOAD_SIZE_MB` | `50` | Maximum upload file size |
| `WORKERS` | `4` | Gunicorn worker processes |
| `UVICORN_PORT` | `4748` | Service port |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_DIR` | `logs` | Log directory |
| `LOG_MAX_BYTES` | `10485760` | Maximum log file size (10MB) |
| `LOG_BACKUP_COUNT` | `5` | Number of log backup files |
| `MAX_ATOMS_WARNING` | `1000` | Warning threshold for structure size |
| `MAX_ATOMS_LIMIT` | `10000` | Hard limit for structure size |
| `SUPPORTED_FORMATS` | `.xyz,.cif,.vasp,.poscar,.contcar` | Supported file formats |

---

## 🎯 GPU Support

The service automatically detects available compute devices:

1. **Auto Detection** (`DEVICE=auto`):
   - Priority: CUDA GPU > Apple Silicon MPS > CPU

2. **Manual Override**:
   - `DEVICE=cpu` - Force CPU
   - `DEVICE=cuda` - Force CUDA
   - `DEVICE=mps` - Force MPS

**Check GPU Status:**
```bash
curl http://localhost:4748/info
```

---

## 🔒 Security Features

- ✅ File size limit (default 50MB)
- ✅ Path traversal protection
- ✅ File type validation (.xyz/.cif/.vasp/.poscar/.contcar)
- ✅ Structure size validation (prevents oversized structures)
- ✅ Standardized error codes (MACE_xxx)
- ✅ Comprehensive exception handling
- ✅ Health check endpoints

---

## 📖 References

- Batzner et al., *Nature Communications* (2022)
- [MACE](https://github.com/ACEsuit/mace)
- [ASE](https://wiki.fysik.dtu.dk/ase/)

## 👤 Author

Li Shibo · 2025  
MIT License