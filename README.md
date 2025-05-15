# MACEOPT：基于 MACE 的几何优化 API 服务

这是一个轻量级的 FastAPI 服务，用于对原子结构（如 MOF、分子、材料）进行几何优化。优化过程基于 MACE（神经力场）和 ASE（结构优化器），支持 `.xyz` 文件上传，支持 Docker 部署，并提供优化结果下载。

---

## 🚀 功能特点

- 支持 `.xyz` 结构文件上传
- 使用 MACE-MP-0 力场 + ASE BFGS 优化算法
- 可配置的收敛精度（`fmax`）和运行设备（`cpu` / `cuda`）
- 优化结构自动保存至 `output/` 目录
- 支持下载优化结果
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
uvicorn app.main:app --reload --port 8000
```

浏览器打开 [http://localhost:4747/docs](http://localhost:4747/docs) 进入 Swagger UI 测试页面。

---

## 🔁 API 接口说明

### ✅ POST `/optimize` - 结构优化接口

| 参数名          | 类型     | 是否必填 | 示例         |
|------------------|----------|----------|--------------|
| structure_file   | 文件     | ✅       | `test.xyz`   |
| fmax             | float    | ❌       | `0.1`        |
| device           | string   | ❌       | `cpu`        |

**返回示例：**

```json
{
  "success": true,
  "n_atoms": 42,
  "input_file": "/tmp/tmpabc.xyz",
  "output_file": "output/tmpabc_opt.xyz",
  "fmax": 0.1,
  "device": "cpu"
}
```

---

### ⬇️ GET `/download?filename=xxx_opt.xyz` - 下载优化结果

传入输出文件名，即可下载 `.xyz` 优化结构。

---

## 🐳 Docker 容器部署

### 构建镜像

```bash
docker build -t maceopt .
```

### 启动服务

```bash
docker run -it --rm -p 4747:8000 maceopt
```

然后访问：`http://localhost:4747/docs`

---

## 📁 项目结构说明

```
maceopt/
├── app/
│   ├── main.py          # FastAPI 启动入口
│   ├── api.py           # 接口定义
│   ├── parser.py        # 参数解析与验证
│   ├── core.py          # 优化核心逻辑（MACE + ASE）
│   ├── utils.py         # rich 日志封装
│   └── config.py        # 默认参数配置
├── models/              # 存放 MACE 模型文件
├── examples/            # 示例结构文件
├── output/              # 优化后输出文件
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

石博 Li Shibo · 2025  
MIT 开源许可证
