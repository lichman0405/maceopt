# 使用官方带 PyTorch 的基础镜像（CPU-only）
FROM pytorch/pytorch:2.2.2-cpu

# 设置工作目录
WORKDIR /app

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝代码
COPY app/ app/
COPY models/ models/
COPY examples/ examples/

# 输出目录
RUN mkdir -p output

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
