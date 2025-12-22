
<div align="center">
  <a href="https://github.com/lichman0405/maceopt.git">
    <img src="assets/edit_logo.png" alt="Logo" width="200px">
  </a>

  <h1 align="center">MACEOPT API Service</h1>

  <p align="center">
    这是一个轻量级的 FastAPI 服务，用于对原子结构（如 MOF、分子、材料）进行几何优化。优化过程基于 MACE（神经力场）和 ASE（结构优化器），支持 `.xyz` 文件上传，优化结构将自动按 session 保存为标准 `.xyz` 和含力场信息的 `.extxyz`，支持下载与结果追踪。
    <br>
    <a href="./README-en.md"><strong>English</strong></a>
    ·
    <a href="https://github.com/lichman0405/maceopt.git/issues">报告 Bug</a>
    ·
    <a href="https://github.com/lichman0405/maceopt.git/issues">提出新特性</a>
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

## 🚀 功能特点

- ✅ 支持 `.xyz` 结构文件上传
- ✅ 使用 MACE-MP-0 力场 + ASE BFGS 优化算法
- ✅ **自动GPU检测**（CUDA/MPS/CPU智能切换）
- ✅ 自动创建独立 session 目录保存优化任务
- ✅ 优化输出包含：
  - `optimized.xyz`（标准结构）
  - `optimized.extxyz`（附带能量、受力、应力等信息）
- ✅ 返回完整结构物理字段（如 energy、stress、pbc、forces 等）
- ✅ 丰富终端日志输出（基于 rich）
- ✅ 支持 Docker 一键部署
- ✅ 环境变量配置支持
- ✅ 健康检查端点
- ✅ 文件大小验证
- ✅ 完善的异常处理
- ✅ 生产级 Gunicorn 部署

---

## 📦 安装步骤

```bash
git clone https://github.com/lichman0405/maceopt.git
cd maceopt
pip install -r requirements.txt
```

### 配置环境变量（可选）

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，自定义配置
# DEVICE=auto          # auto/cpu/cuda/mps - GPU自动检测
# MAX_UPLOAD_SIZE_MB=50
# WORKERS=4
```

---

## 🧪 本地运行

### 开发模式（单进程）

```bash
uvicorn app.main:app --reload --port 4748
```

### 生产模式（多进程，推荐）

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:4748 \
  --timeout 300
```

浏览器打开 [http://localhost:4748/docs](http://localhost:4748/docs) 进入 Swagger UI 测试页面。

### 健康检查

```bash
# 检查服务状态
curl http://localhost:4748/health

# 获取服务器信息（包括GPU信息）
curl http://localhost:4748/info
```

---

## 🔁 API 接口说明

### ✅ GET `/health` - 健康检查

返回服务健康状态，用于监控和负载均衡。

**返回示例：**
```json
{
  "status": "healthy",
  "service": "maceopt",
  "version": "0.3.0"
}
```

### ✅ GET `/info` - 服务器信息

返回服务器配置信息，包括GPU检测结果。

**返回示例：**
```json
{
  "service": "MACEOPT Geometry Optimization API",
  "version": "0.3.0",
  "model_path": "models/mace_agnesi_medium.model",
  "device": "CUDA",
  "max_upload_size_mb": 50,
  "supported_formats": [".xyz"],
  "gpu_info": {
    "name": "NVIDIA GeForce RTX 4090",
    "memory_total_gb": 24.0,
    "cuda_version": "12.1"
  }
}
```

### ✅ POST `/optimize` - 结构优化接口

| 参数名          | 类型     | 是否必填 | 示例         | 说明 |
|------------------|----------|----------|--------------|------|
| structure_file   | 文件     | ✅       | `test.xyz`   | 原子结构文件 |
| fmax             | float    | ❌       | `0.1`        | 收敛阈值 (eV/Å) |
| device           | string   | ❌       | `auto`       | `auto`/`cpu`/`cuda`/`mps` |

**返回示例（节选）：**

```json
{
  "success": true,
  "n_atoms": 3,
  "input_file": "/tmp/tmpabc.xyz",
  "output_file": "output/session_8f2d4b1a/optimized.xyz",
  "output_extxyz": "output/session_8f2d4b1a/optimized.extxyz",
  "energy": -14.26,
  "free_energy": -14.26,
  "stress": [...],
  "pbc": [false, false, false],
  "properties": {
    "species": "S:1",
    "pos": "R:3",
    "forces": "R:3"
  },
  "download_links": {
    "xyz": "/download?path=session_8f2d4b1a/optimized.xyz",
    "extxyz": "/download?path=session_8f2d4b1a/optimized.extxyz"
  }
}
```

---

### ⬇️ GET `/download?path=...` - 下载优化结果

使用 `download_links` 字段提供的路径进行结构文件下载：

```bash
curl -O "http://localhost:4748/download?path=session_8f2d4b1a/optimized.xyz"
curl -O "http://localhost:4748/download?path=session_8f2d4b1a/optimized.extxyz"
```

---

## 🧪 快速测试

### 基础测试流程

```bash
# 1. 启动服务
uvicorn app.main:app --reload --port 4748

# 2. 健康检查（新窗口）
curl http://localhost:4748/health

# 3. 查看GPU信息
curl http://localhost:4748/info

# 4. 测试优化
curl -X POST http://localhost:4748/optimize \
  -F "structure_file=@examples/h2o.xyz" \
  -F "fmax=0.1" \
  -F "device=auto"

# 5. 浏览器访问 Swagger UI
# http://localhost:4748/docs
```

### 预期结果

- ✅ `/health` 返回 `{"status": "healthy"}`
- ✅ `/info` 显示设备类型（CUDA/CPU）
- ✅ `/optimize` 返回优化结果和下载链接
- ✅ `output/` 目录下生成 session 文件夹

---

## 🐳 Docker 容器部署

### 使用 Docker Compose（推荐）

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 手动构建镜像

```bash
docker build -t maceopt .
```

### 启动服务

**CPU版本：**
```bash
docker run -it --rm -p 4748:8000 -v $(pwd)/output:/app/output maceopt
```

**GPU版本（需要 nvidia-docker）：**
```bash
docker run -it --rm --gpus all \
  -p 4748:8000 \
  -v $(pwd)/output:/app/output \
  -e DEVICE=auto \
  maceopt
```

然后访问：`http://localhost:4748/docs`

---

## 📁 项目结构说明

```
maceopt/
├── app/
│   ├── main.py          # FastAPI 启动入口
│   ├── api.py           # 接口定义 + 路由绑定
│   ├── parser.py        # 参数解析 + session 路径构造
│   ├── core.py          # 核心优化逻辑（MACE + ASE + GPU检测）
│   ├── utils.py         # rich 日志封装
│   └── config.py        # 默认模型/路径配置 + 环境变量
├── models/              # 存放 MACE 训练模型
├── examples/            # 示例输入结构
├── output/              # 自动生成优化 session 目录
├── .env.example         # 环境变量配置模板
├── requirements.txt     # Python 依赖
├── Dockerfile           # Docker 镜像定义
├── docker-compose.yml   # Docker Compose 配置
└── README.md
```

---

## ⚙️ 配置说明

所有配置项可通过环境变量设置（`.env` 文件）：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `MACE_MODEL_PATH` | `models/mace_agnesi_medium.model` | MACE模型路径 |
| `OUTPUT_DIR` | `output` | 输出目录 |
| `DEVICE` | `auto` | 计算设备（auto自动检测） |
| `MAX_UPLOAD_SIZE_MB` | `50` | 最大上传文件大小 |
| `WORKERS` | `4` | Gunicorn worker进程数 |
| `UVICORN_PORT` | `4748` | 服务端口 |
| `LOG_LEVEL` | `INFO` | 日志级别 |

---

## 🎯 GPU 支持

服务会自动检测可用的计算设备：

1. **自动检测** (`DEVICE=auto`)：
   - 优先使用 CUDA GPU
   - 其次使用 Apple Silicon MPS
   - 最后回退到 CPU

2. **手动指定**：
   - `DEVICE=cpu` - 强制使用CPU
   - `DEVICE=cuda` - 强制使用CUDA
   - `DEVICE=mps` - 强制使用MPS

**检查GPU状态：**
```bash
curl http://localhost:4748/info
```

---

## 🔒 安全特性

- ✅ 文件大小限制（默认50MB）
- ✅ 路径遍历保护
- ✅ 文件类型验证（仅支持.xyz）
- ✅ 完整的异常处理
- ✅ 健康检查端点

---

## 📚 参考文献

本项目基于以下模型与工具：

- Batzner et al., *E(3)-equivariant Graph Neural Networks for Data-Efficient and Accurate Interatomic Potentials*, Nature Communications, 2022
- [MACE 模型](https://github.com/ACEsuit/mace)
- [ASE 优化器](https://wiki.fysik.dtu.dk/ase/)

---

## 👤 作者

Li Shibo · 2025  
MIT 开源许可证
