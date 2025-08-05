#!/bin/bash

echo "正在创建BMI MCP服务的独立Python环境..."
echo

# 创建虚拟环境
echo "1. 创建虚拟环境..."
python3 -m venv bmi_mcp_env
if [ $? -ne 0 ]; then
    echo "错误：无法创建虚拟环境"
    exit 1
fi

# 激活虚拟环境
echo "2. 激活虚拟环境..."
source bmi_mcp_env/bin/activate
if [ $? -ne 0 ]; then
    echo "错误：无法激活虚拟环境"
    exit 1
fi

# 升级pip
echo "3. 升级pip..."
python -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "错误：无法升级pip"
    exit 1
fi

# 安装依赖
echo "4. 安装MCP依赖..."
pip install mcp==1.12.2
if [ $? -ne 0 ]; then
    echo "错误：无法安装MCP库"
    exit 1
fi

echo "5. 安装其他依赖..."
pip install uvicorn fastapi flask gunicorn
if [ $? -ne 0 ]; then
    echo "错误：无法安装其他依赖"
    exit 1
fi

# 导出依赖列表
echo "6. 导出依赖列表..."
pip freeze > requirements_clean.txt
if [ $? -ne 0 ]; then
    echo "警告：无法导出依赖列表"
fi

echo
echo "环境创建完成！"
echo "要激活环境，请运行：source bmi_mcp_env/bin/activate"
echo "要运行MCP服务，请执行：python mcp_stdio.py"
echo "要退出环境，请执行：deactivate"