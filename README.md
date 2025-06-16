
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

- 支持 `.xyz` 结构文件上传
- 使用 MACE-MP-0 力场 + ASE BFGS 优化算法
- 自动创建独立 session 目录保存优化任务
- 优化输出包含：
  - `optimized.xyz`（标准结构）
  - `optimized.extxyz`（附带能量、受力、应力等信息）
- 返回完整结构物理字段（如 energy、stress、pbc、forces 等）
- 丰富终端日志输出（基于 rich）
- 支持 Docker 一键部署

---

## 📦 安装步骤

```bash
git clone https://github.com/your-org/maceopt.git
cd maceopt
pip install -r requirements.txt
```

---

## 🧪 本地运行

```bash
uvicorn app.main:app --reload --port 4748
```

浏览器打开 [http://localhost:4748/docs](http://localhost:4748/docs) 进入 Swagger UI 测试页面。

---

## 🔁 API 接口说明

### ✅ POST `/optimize` - 结构优化接口

| 参数名          | 类型     | 是否必填 | 示例         |
|------------------|----------|----------|--------------|
| structure_file   | 文件     | ✅       | `test.xyz`   |
| fmax             | float    | ❌       | `0.1`        |
| device           | string   | ❌       | `cpu`        |

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

## 🐳 Docker 容器部署

### 构建镜像

```bash
docker build -t maceopt .
```

### 启动服务

```bash
docker run -it --rm -p 4748:8000 maceopt
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
│   ├── core.py          # 核心优化逻辑（MACE + ASE）
│   ├── utils.py         # rich 日志封装
│   └── config.py        # 默认模型/路径配置
├── models/              # 存放 MACE 训练模型
├── examples/            # 示例输入结构
├── output/              # 自动生成优化 session 目录
├── requirements.txt
├── Dockerfile
└── README.md
```

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
