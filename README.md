<div align="center">
  <a href="https://github.com/lichman0405/maceopt.git">
    <img src="assets/edit_logo.png" alt="Logo" width="200px">
  </a>

  <h1 align="center">MACEOPT API 服务</h1>

  <p align="center">
    这是一个轻量级的 FastAPI 服务，用于对原子结构（如 MOF、分子、材料）进行几何优化。该服务结合了 MACE 神经力场与 ASE 优化器，支持上传<code>.cif</code> 结构文件。优化任务的结果将按会话（session）自动保存，并提供优化后的 <code>.cif</code>（标准结构）和 <code>.extcif</code>（含能量、力、应力等信息）文件，支持下载与结果追踪。
    <br>
    <a href="README-en.md"><strong>English</strong></a>
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

- 支持上传结构文件 (`.cif`)
- 使用 MACE-MP-0 力场 + ASE BFGS 优化算法
- 自动为每个优化任务创建独立的会话（session）目录
- 优化输出包含：
  - `optimized.cif`（标准结构文件）
  - `optimized.extcif`（包含能量、受力、应力等附加物理数据）
- 返回完整的物理量（如能量、应力、周期性边界条件、力等）
- 丰富的终端日志输出（基于 rich）
- 支持 Docker 一键部署

---

## 📦 安装步骤

```bash
git clone https://github.com/lichman0405/maceopt.git
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

### ✅ POST `/optimize`

此接口接收一个结构文件，并使用 MACE 力场对其进行几何优化。

**请求体 (Request Body):**

| 参数 | 类型 | 是否必须 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `structure_file` | file | ✅ | - | 待优化的结构文件 (`.cif`)。 |
| `fmax` | float | ❌ | `0.1` | 优化的收敛阈值，表示任何原子上的最大力。 |
| `steps` | int | ❌ | `100` | 最大优化步数。 |
| `optimizer_name` | string | ❌ | `BFGS` | 用于计算的 ASE 优化器名称。 |
| `device` | string | ❌ | `cpu` | 运行 MACE 模型的设备 (`cpu` 或 `cuda`)。 |

**响应体 (Response Body, 成功时):**

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

- **`session_id`**: 优化任务的唯一标识符。
- **`message`**: 表示结果的状态消息。
- **`optimized_structure_cif`**: 优化后结构的 `.cif` 格式文件内容。
- **`optimized_structure_extcif`**: 优化后结构的 `.extcif` 格式文件内容，包含额外的物理数据。
- **`download_link_cif`**: 用于下载 `.cif` 文件的直接链接。
- **`download_link_extcif`**: 用于下载 `.extcif` 文件的直接链接。
- **`log_output`**: 优化过程中的详细日志。

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
│   ├── api.py           # 接口定义与路由
│   ├── parser.py        # 参数解析与会话路径构造
│   ├── core.py          # 核心优化逻辑 (MACE + ASE)
│   ├── utils.py         # rich 日志工具
│   └── config.py        # 默认模型与路径配置
├── models/              # 存放 MACE 训练模型
├── examples/            # 示例输入结构
├── output/              # 自动生成的优化会话目录
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