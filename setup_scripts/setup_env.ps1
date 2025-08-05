# BMI MCP Environment Setup Script
Write-Host "正在创建BMI MCP服务的独立Python环境..." -ForegroundColor Green
Write-Host ""

# 检查Python是否已安装
try {
    $pythonVersion = python --version
    Write-Host "找到Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "错误：未找到Python。请先安装Python 3.8或更高版本。" -ForegroundColor Red
    exit 1
}

# 创建虚拟环境
Write-Host "1. 创建虚拟环境..." -ForegroundColor Yellow
python -m venv bmi_mcp_env
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误：无法创建虚拟环境" -ForegroundColor Red
    exit 1
}

# 激活虚拟环境
Write-Host "2. 激活虚拟环境..." -ForegroundColor Yellow
& .\bmi_mcp_env\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误：无法激活虚拟环境" -ForegroundColor Red
    exit 1
}

# 升级pip
Write-Host "3. 升级pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误：无法升级pip" -ForegroundColor Red
    exit 1
}

# 安装依赖
Write-Host "4. 安装MCP依赖..." -ForegroundColor Yellow
pip install mcp==1.12.2
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误：无法安装MCP库" -ForegroundColor Red
    exit 1
}

Write-Host "5. 安装其他依赖..." -ForegroundColor Yellow
pip install uvicorn fastapi flask gunicorn
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误：无法安装其他依赖" -ForegroundColor Red
    exit 1
}

# 导出依赖列表
Write-Host "6. 导出依赖列表..." -ForegroundColor Yellow
pip freeze > requirements_clean.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "警告：无法导出依赖列表" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "环境创建完成！" -ForegroundColor Green
Write-Host "要激活环境，请运行：.\bmi_mcp_env\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "要运行MCP服务，请执行：python mcp_stdio.py" -ForegroundColor Cyan
Write-Host "要退出环境，请执行：deactivate" -ForegroundColor Cyan