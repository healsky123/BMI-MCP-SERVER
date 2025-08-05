@echo off
echo 正在创建BMI MCP服务的独立Python环境...
echo.

REM 创建虚拟环境
echo 1. 创建虚拟环境...
python -m venv bmi_mcp_env
if %errorlevel% neq 0 (
    echo 错误：无法创建虚拟环境
    exit /b 1
)

REM 激活虚拟环境
echo 2. 激活虚拟环境...
call bmi_mcp_env\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo 错误：无法激活虚拟环境
    exit /b 1
)

REM 升级pip
echo 3. 升级pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo 错误：无法升级pip
    exit /b 1
)

REM 安装依赖
echo 4. 安装MCP依赖...
pip install mcp==1.12.2
if %errorlevel% neq 0 (
    echo 错误：无法安装MCP库
    exit /b 1
)

echo 5. 安装其他依赖...
pip install uvicorn fastapi flask gunicorn
if %errorlevel% neq 0 (
    echo 错误：无法安装其他依赖
    exit /b 1
)

REM 导出依赖列表
echo 6. 导出依赖列表...
pip freeze > requirements_clean.txt
if %errorlevel% neq 0 (
    echo 警告：无法导出依赖列表
)

echo.
echo 环境创建完成！
echo 要激活环境，请运行：bmi_mcp_env\Scripts\activate.bat
echo 要运行MCP服务，请执行：python mcp_stdio.py
echo 要退出环境，请执行：deactivate