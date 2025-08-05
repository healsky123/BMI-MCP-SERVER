# BMI Calculator MCP Service

全人群BMI计算器MCP服务，支持从儿童到老年人的BMI计算和评价分类。
注：6-20岁的在校学生有专门的BMI评价标准，与成年人标准有所不同，
且严格细分目前大模型（LLM)学到的知识里都只有一个笼统的评价标准，
不利于对健康体重的评价分类,本服务为大模型能获取更细分的健康体重
评价分类提供了精确的计算和评价，为健康体重相关提问和应用项目增
加一个实用的科学工具。

## 功能特点

- 支持全年龄段（6岁至79岁）BMI计算
- 根据年龄和性别提供个性化BMI标准
- 提供标准MCP工具接口
- 支持Streamable HTTP和STDIO两种通信方式

## MCP工具接口使用指南

为了提高使用效率，我们提供了三个专门的工具，根据不同的使用场景选择合适的工具：

### calculate_bmi（推荐优先使用）
**功能**：一次性计算BMI值并获取分类评价
**使用场景**：当您需要同时获取BMI值和分类时使用，这是功能最全面的工具

```bash
# 调用calculate_bmi工具（一次性获取BMI值和分类）
# 通过MCP客户端调用
{
  "method": "calculate_bmi",
  "params": {
    "age": 25,
    "gender": "male",
    "weight": 70,
    "height": 1.75
  }
}
# 返回: {"bmi": 22.9, "category": "normal"}
```

### calculate_bmi_value
**功能**：仅计算BMI值
**使用场景**：当您只需要BMI数值，不需要分类评价时使用

```bash
# 调用calculate_bmi_value工具（只需要BMI数值）
# 通过MCP客户端调用
{
  "method": "calculate_bmi_value",
  "params": {
    "weight": 70,
    "height": 1.75
  }
}
# 返回: 22.9
```

### get_bmi_category
**功能**：根据已知BMI值获取分类
**使用场景**：当您已经知道BMI值，只需要获取对应的分类评价时使用

```bash
# 调用get_bmi_category工具（已知BMI值，获取分类）
# 通过MCP客户端调用
{
  "method": "get_bmi_category",
  "params": {
    "age": 25,
    "gender": "male",
    "bmi": 22.9
  }
}
# 返回: "normal"
```

## 工具详细说明

### calculate_bmi
计算BMI值和分类
```
age: 年龄（整数）
gender: 性别（"male" 或 "female"）
weight: 体重（公斤，数值）
height: 身高（米，数值）
```

### get_bmi_category
根据年龄、性别和BMI值获取分类
```
age: 年龄（整数）
gender: 性别（"male" 或 "female"）
bmi: BMI值（数值）
```

### calculate_bmi_value
计算BMI值（不考虑年龄和性别）
```
weight: 体重（公斤，数值）
height: 身高（米，数值）
```

### 资源接口

### bmi://standards
获取BMI标准信息

## 环境准备

### 自动环境设置（推荐）
项目提供了环境设置脚本，可根据您的操作系统选择：

#### Windows系统
```cmd
# 使用批处理脚本
setup_env.bat

# 或使用PowerShell脚本
PowerShell -ExecutionPolicy Bypass -File setup_env.ps1
```

#### macOS/Linux系统
```bash
chmod +x setup_env.sh
./setup_env.sh
```

### 手动环境设置
如果脚本无法正常工作，可以手动执行以下步骤：

```bash
# 1. 创建虚拟环境
python -m venv bmi_mcp_env

# 2. 激活虚拟环境
# Windows:
bmi_mcp_env\Scripts\activate
# macOS/Linux:
source bmi_mcp_env/bin/activate

# 3. 升级pip
python -m pip install --upgrade pip

# 4. 安装依赖
pip install -r requirements.txt
```

## 部署方式（标准MCP服务器）

### STDIO方式（推荐用于测试和本地使用）
```bash
# 确保已激活虚拟环境并安装依赖
python mcp_stdio.py
```

### STREAMABLE HTTP方式（推荐用于生产环境）
```bash
# 确保已激活虚拟环境并安装依赖
python bmi_mcp_http.py
```

## 服务配置（Server config）

```json
{
  "name": "BMI Calculator",
  "description": "全人群BMI计算器MCP服务，支持从儿童到老年人的BMI计算和分类",
  "version": "1.0.0",
  "transport": {
    "stdio": {
      "type": "stdio",
      "command": "python",
      "args": ["mcp_stdio.py"],
      "cwd": "."
    },
    "http": {
      "type": "http",
      "url": "http://localhost:8000",
      "health_check_path": "/health"
    }
  },
  "tools": [
    {
      "name": "calculate_bmi",
      "description": "计算BMI值和分类",
      "input_schema": {
        "type": "object",
        "properties": {
          "age": {
            "type": "integer",
            "description": "年龄（整数，6-79岁）"
          },
          "gender": {
            "type": "string",
            "enum": ["male", "female"],
            "description": "性别（\"male\" 或 \"female\"）"
          },
          "weight": {
            "type": "number",
            "description": "体重（公斤，数值）"
          },
          "height": {
            "type": "number",
            "description": "身高（米，数值）"
          }
        },
        "required": ["age", "gender", "weight", "height"]
      }
    },
    {
      "name": "get_bmi_category",
      "description": "根据年龄、性别和BMI值获取分类",
      "input_schema": {
        "type": "object",
        "properties": {
          "age": {
            "type": "integer",
            "description": "年龄（整数，6-79岁）"
          },
          "gender": {
            "type": "string",
            "enum": ["male", "female"],
            "description": "性别（\"male\" 或 \"female\"）"
          },
          "bmi": {
            "type": "number",
            "description": "BMI值（数值）"
          }
        },
        "required": ["age", "gender", "bmi"]
      }
    },
    {
      "name": "calculate_bmi_value",
      "description": "计算BMI值（不考虑年龄和性别）",
      "input_schema": {
        "type": "object",
        "properties": {
          "weight": {
            "type": "number",
            "description": "体重（公斤，数值）"
          },
          "height": {
            "type": "number",
            "description": "身高（米，数值）"
          }
        },
        "required": ["weight", "height"]
      }
    }
  ],
  "resources": [
    {
      "uri": "bmi://standards",
      "name": "BMI标准信息",
      "description": "获取BMI标准信息",
      "mimeType": "text/plain"
    }
  ]
}
```

## 环境变量配置

本服务不需要特殊的环境变量配置即可运行。如需自定义配置，可设置以下环境变量：

```json
{
  "env": {
    "PYTHONPATH": ".",
    "LOG_LEVEL": "INFO"
  }
}
```

## 服务地址和端口

默认情况下，HTTP服务运行在以下地址：
- 地址: `http://localhost:8000`
- 健康检查端点: `http://localhost:8000/health`

## 客户端请求标准示例

### 工具调用示例（通过MCP协议）
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "calculate_bmi",
  "params": {
    "age": 25,
    "gender": "male",
    "weight": 70,
    "height": 1.75
  }
}
```

## 使用示例

### 作为MCP服务使用
服务启动后，可以通过支持MCP协议的客户端调用工具。

### 直接调用（开发测试）
```python
from bmiMCP import BMIEvaluator

# 计算BMI
evaluator = BMIEvaluator()
result = evaluator.evaluate(25, "male", 70, 1.75)
print(result)  # {'bmi': 22.9, 'category': 'normal'}

## 许可证

本项目采用MIT许可证，详情请见 [LICENSE](LICENSE) 文件。
