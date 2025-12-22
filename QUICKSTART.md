# Quick Start Guide - MACEOPT v0.3.0

## 🚀 快速开始（Windows）

### 步骤 1：安装依赖

```powershell
# 确保在正确的分支
git branch

# 应该显示：* feature/performance-optimization

# 安装Python依赖
pip install -r requirements.txt
```

### 步骤 2：启动服务

```powershell
# 开发模式（推荐初次测试）
uvicorn app.main:app --reload --port 4748
```

### 步骤 3：验证服务

打开新的PowerShell窗口：

```powershell
# 健康检查
curl http://localhost:4748/health

# 查看GPU信息
curl http://localhost:4748/info
```

### 步骤 4：测试优化

```powershell
# 优化水分子
curl -X POST http://localhost:4748/optimize `
  -F "structure_file=@examples/h2o.xyz" `
  -F "fmax=0.1" `
  -F "device=auto"
```

### 步骤 5：查看结果

```powershell
# 查看Swagger UI（推荐）
# 浏览器打开：http://localhost:4748/docs

# 或查看输出目录
ls output/
```

---

## 🆕 新功能测试

### GPU 自动检测

服务启动时自动检测GPU：
- ✅ 有GPU：自动使用CUDA加速
- ✅ 无GPU：自动使用CPU

查看检测结果：
```powershell
curl http://localhost:4748/info | ConvertFrom-Json | ConvertTo-Json
```

### 环境变量配置

```powershell
# 创建配置文件（可选）
copy .env.example .env

# 编辑 .env 自定义配置
notepad .env
```

可配置项：
- `DEVICE=auto` - GPU检测模式
- `MAX_UPLOAD_SIZE_MB=50` - 文件大小限制
- `WORKERS=4` - 进程数

---

## ⚠️ 注意事项

1. **Windows不支持Gunicorn**
   - 使用 `uvicorn` 启动即可
   - Docker部署会自动使用Gunicorn

2. **GPU加速**
   - 需要NVIDIA GPU + CUDA
   - 自动检测，无需配置

3. **测试数据**
   - 使用 `examples/h2o.xyz` 测试
   - 或使用 `examples/ABAVIJ_clean.cif`（如果支持）

---

## 📖 完整文档

- 详细测试：查看 [TESTING.md](TESTING.md)
- 更新日志：查看 [CHANGELOG.md](CHANGELOG.md)
- 完整文档：查看 [README.md](README.md)

---

## 🐛 遇到问题？

```powershell
# 1. 检查Python版本（需要3.10+）
python --version

# 2. 检查依赖安装
pip list | Select-String "mace|ase|fastapi"

# 3. 检查端口占用
netstat -ano | findstr :4748

# 4. 查看详细日志
# 服务运行的终端会显示所有日志
```

---

## ✅ 验证清单

完成以下验证后，新版本可以使用：

- [ ] 服务成功启动
- [ ] `/health` 端点返回正常
- [ ] `/info` 显示正确的设备信息
- [ ] 成功优化 `h2o.xyz`
- [ ] 能够下载结果文件
- [ ] Swagger UI 正常显示

---

祝使用愉快！🎉

有问题请查看 [TESTING.md](TESTING.md) 获取详细帮助。
