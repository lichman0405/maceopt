# 测试指南 - v0.3.0

本文档提供详细的测试步骤，确保所有新功能正常工作。

## 📋 测试前准备

### 1. 安装依赖

```bash
# 确保你在 feature/performance-optimization 分支
git branch

# 安装/更新依赖
pip install -r requirements.txt
```

### 2. 配置环境变量（可选）

```bash
# 复制配置模板
copy .env.example .env

# 编辑 .env 自定义配置（或使用默认值）
```

---

## ✅ 功能测试清单

### 测试 1: GPU 自动检测

**Windows 测试命令：**

```powershell
# 启动服务
uvicorn app.main:app --reload --port 4748
```

**预期结果：**
- 启动日志中显示GPU检测信息
- 如果有NVIDIA GPU，显示：`✔ GPU Detected: [GPU名称]`
- 如果没有GPU，显示：`⚠ No GPU detected, using CPU`

**验证命令：**
```powershell
# 访问info端点查看GPU信息
curl http://localhost:4748/info
```

**预期返回（有GPU）：**
```json
{
  "service": "MACEOPT Geometry Optimization API",
  "version": "0.3.0",
  "device": "CUDA",
  "gpu_info": {
    "name": "NVIDIA xxx",
    "memory_total_gb": xx.x,
    "cuda_version": "x.x"
  }
}
```

**预期返回（无GPU）：**
```json
{
  "service": "MACEOPT Geometry Optimization API",
  "version": "0.3.0",
  "device": "CPU"
}
```

---

### 测试 2: 健康检查端点

```powershell
curl http://localhost:4748/health
```

**预期返回：**
```json
{
  "status": "healthy",
  "service": "maceopt",
  "version": "0.3.0"
}
```

---

### 测试 3: 结构优化（基本功能）

```powershell
# 使用示例文件测试
curl -X POST http://localhost:4748/optimize `
  -F "structure_file=@examples/h2o.xyz" `
  -F "fmax=0.1" `
  -F "device=auto"
```

**预期结果：**
- 返回成功的JSON响应
- 包含 `"success": true`
- 包含能量、应力等物理信息
- 包含下载链接

**检查输出文件：**
```powershell
# 查看output目录
ls output/

# 应该看到新的 session_xxxxxxxx 目录
# 里面包含 original.xyz, optimized.xyz, optimized.extxyz
```

---

### 测试 4: 文件大小验证

```powershell
# 创建一个大文件（>50MB）
# Windows PowerShell:
$null | Set-Content -Path "large_file.xyz" -Value ("0`n`nH 0 0 0`n" * 5000000)

# 尝试上传
curl -X POST http://localhost:4748/optimize `
  -F "structure_file=@large_file.xyz" `
  -F "fmax=0.1"
```

**预期结果：**
- 返回 HTTP 413 错误
- 错误信息：`File size exceeds maximum allowed size of 50 MB`

---

### 测试 5: 设备参数验证

**测试强制使用CPU：**
```powershell
curl -X POST http://localhost:4748/optimize `
  -F "structure_file=@examples/h2o.xyz" `
  -F "fmax=0.1" `
  -F "device=cpu"
```

**预期结果：**
- 成功返回
- `"device": "cpu"` 在响应中

---

### 测试 6: 下载功能

```powershell
# 从上一次优化结果中获取 session ID
# 例如：session_abc12345

# 下载 .xyz 文件
curl -o optimized.xyz "http://localhost:4748/download?path=session_abc12345/optimized.xyz"

# 下载 .extxyz 文件
curl -o optimized.extxyz "http://localhost:4748/download?path=session_abc12345/optimized.extxyz"
```

**预期结果：**
- 文件成功下载
- 文件内容正确

---

### 测试 7: 错误处理

**测试不支持的文件格式：**
```powershell
# 创建一个.txt文件
echo "test" > test.txt

curl -X POST http://localhost:4748/optimize `
  -F "structure_file=@test.txt" `
  -F "fmax=0.1"
```

**预期结果：**
- 返回 HTTP 400 错误
- 错误信息：`Only .xyz files are supported`

**测试无效路径下载：**
```powershell
curl "http://localhost:4748/download?path=../../etc/passwd"
```

**预期结果：**
- 返回 HTTP 400 或 404 错误
- 路径安全验证生效

---

## 🧪 Swagger UI 测试

1. 打开浏览器访问：http://localhost:4748/docs
2. 查看新增的端点：
   - `GET /health`
   - `GET /info`
   - `POST /optimize` (更新了参数说明)
   - `GET /download`

3. 使用 Swagger UI 界面测试所有端点

---

## 🔍 回归测试

**确保原有功能未受影响：**

1. ✅ 基本优化功能正常
2. ✅ Session 管理正常
3. ✅ 文件上传/下载正常
4. ✅ 日志输出正常
5. ✅ 错误处理正常

---

## 🐛 已知问题

### Windows特定问题

1. **Gunicorn不支持Windows**
   - 解决方案：Windows下使用 `uvicorn` 启动
   - 生产环境建议使用 Linux/Docker

2. **PowerShell curl 别名**
   - PowerShell的`curl`实际是`Invoke-WebRequest`
   - 如果遇到问题，使用 `curl.exe` 或安装真正的curl

---

## 📊 性能测试（可选）

**简单压力测试：**

```powershell
# 使用 Apache Bench (需要单独安装)
ab -n 100 -c 10 http://localhost:4748/health

# 或使用 PowerShell 循环
1..10 | ForEach-Object {
    Measure-Command {
        curl http://localhost:4748/health
    }
}
```

---

## ✅ 测试完成检查表

- [ ] GPU自动检测正常
- [ ] 健康检查端点可访问
- [ ] 服务器信息端点返回正确
- [ ] 基本优化功能正常
- [ ] 文件大小限制生效
- [ ] 设备参数正确处理
- [ ] 下载功能正常
- [ ] 错误处理正确
- [ ] Swagger UI 显示正常
- [ ] 所有原有功能正常

---

## 🆘 遇到问题？

### 常见问题排查

**1. 导入错误**
```bash
pip install -r requirements.txt --upgrade
```

**2. 端口被占用**
```powershell
# 更换端口
uvicorn app.main:app --reload --port 8888
```

**3. GPU未检测到**
```powershell
# 检查PyTorch CUDA支持
python -c "import torch; print(torch.cuda.is_available())"
```

**4. 模型文件不存在**
```bash
# 确保模型文件在正确位置
ls models/mace_agnesi_medium.model
```

---

## 📝 测试报告

测试完成后，请记录：

1. ✅ 通过的测试
2. ❌ 失败的测试（如果有）
3. ⚠️ 发现的问题
4. 💡 改进建议

---

## 🔄 回滚方法

如果测试发现问题，可以随时回滚：

```bash
# 切回main分支
git checkout main

# 删除测试分支（可选）
git branch -D feature/performance-optimization
```

---

祝测试顺利！🎉
