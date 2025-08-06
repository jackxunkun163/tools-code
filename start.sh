#!/bin/bash

# 蓝牙技术文章聚合平台启动脚本

echo "============================================================"
echo "蓝牙技术文章聚合平台"
echo "============================================================"

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "错误: 需要Python 3.8或更高版本，当前版本: $python_version"
    exit 1
fi

echo "Python版本检查通过: $python_version"

# 检查依赖包
echo "检查依赖包..."
if ! python3 -c "import flask, requests, beautifulsoup4, schedule, openai" 2>/dev/null; then
    echo "安装依赖包..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 依赖包安装失败"
        exit 1
    fi
fi

echo "依赖包检查通过"

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "创建环境变量文件..."
    cp env_example.txt .env
    echo "请编辑 .env 文件配置必要的参数"
    echo "特别是 OPENAI_API_KEY 需要设置为有效的API密钥"
fi

# 创建日志目录
mkdir -p logs

# 启动程序
echo "启动蓝牙技术文章聚合平台..."
echo "Web界面地址: http://localhost:5000"
echo "按 Ctrl+C 停止程序"
echo "============================================================"

python3 main.py 