# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2025-12-22

### ✨ Added
- **GPU自动检测**: 自动检测并使用CUDA/MPS/CPU，无需手动配置
- **环境变量配置**: 通过`.env`文件管理所有配置项
- **健康检查端点**: 新增 `/health` 端点用于监控
- **服务器信息端点**: 新增 `/info` 端点显示GPU信息和配置
- **文件大小验证**: 限制上传文件大小（默认50MB），防止OOM
- **完善的异常处理**: 所有错误都有明确的HTTP状态码和错误信息
- **Gunicorn支持**: 生产环境推荐使用多进程部署
- **Docker健康检查**: Docker容器内置健康检查

### 🔧 Changed
- 更新API版本至 v0.3.0
- 优化Dockerfile，使用多阶段构建
- 优化docker-compose配置，支持GPU
- device参数默认值从`cpu`改为`auto`
- 增强日志输出，显示GPU检测信息

### 📝 Documentation
- 更新README.md，添加GPU使用说明
- 添加`.env.example`配置模板
- 添加配置说明和安全特性文档
- 添加生产部署建议

### 🛡️ Security
- 添加文件大小限制
- 增强路径验证
- 改进异常处理，避免信息泄露

---

## [0.2.0] - 2025-06-16

### Initial Release
- 基础几何优化功能
- FastAPI RESTful API
- MACE + ASE + BFGS 优化
- Session管理
- Docker支持
- Rich日志输出
