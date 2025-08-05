#!/usr/bin/env python3
from mcp.server.fastmcp import FastMCP
from bmiMCP import BMIEvaluator

# 创建MCP服务实例
mcp = FastMCP("BMICalculator")

# 初始化BMI评估器
evaluator = BMIEvaluator()

@mcp.tool()
def calculate_bmi(age: int, gender: str, weight: float, height: float) -> dict:
    """
    计算BMI值和分类（推荐：需要同时获取BMI值和分类时使用）
    
    使用场景：
    - 当您需要一次性获取BMI值和对应的分类评价时
    - 这是功能最全面的工具，避免分别调用calculate_bmi_value和get_bmi_category
    
    Args:
        age: 年龄（整数，6-79岁）
        gender: 性别（"male" 或 "female"）
        weight: 体重（公斤，数值）
        height: 身高（米，数值）
        
    Returns:
        dict: 包含BMI值和分类的字典
        例如: {"bmi": 22.9, "category": "normal"}
    """
    # 参数验证
    if not isinstance(age, int) or age < 0 or age > 150:
        raise ValueError("年龄必须是0-150之间的整数")
        
    if gender not in ['male', 'female']:
        raise ValueError("性别必须是 'male' 或 'female'")
        
    if not isinstance(weight, (int, float)) or weight <= 0 or weight > 1000:
        raise ValueError("体重必须是0-1000之间的正数")
        
    if not isinstance(height, (int, float)) or height <= 0 or height > 3:
        raise ValueError("身高必须是0-3之间的正数（米）")
    
    # 计算BMI
    result = evaluator.evaluate(age, gender, weight, height)
    return result

@mcp.tool()
def get_bmi_category(age: int, gender: str, bmi: float) -> str:
    """
    根据已知BMI值获取分类（推荐：已知BMI值，只需要分类时使用）
    
    使用场景：
    - 当您已经知道BMI值，只需要获取对应的分类评价时
    - 如果您需要同时获取BMI值和分类，请使用calculate_bmi工具
    
    Args:
        age: 年龄（整数，6-79岁）
        gender: 性别（"male" 或 "female"）
        bmi: 已知的BMI值（数值）
        
    Returns:
        str: BMI分类结果（underweight/normal/overweight/obese）
        例如: "normal"
    """
    # 参数验证
    if not isinstance(age, int) or age < 0 or age > 150:
        raise ValueError("年龄必须是0-150之间的整数")
        
    if gender not in ['male', 'female']:
        raise ValueError("性别必须是 'male' 或 'female'")
        
    if not isinstance(bmi, (int, float)) or bmi <= 0 or bmi > 100:
        raise ValueError("BMI值必须是0-100之间的正数")
    
    # 获取BMI分类
    category = evaluator.get_bmi_category(age, gender, bmi)
    return category

@mcp.tool()
def calculate_bmi_value(weight: float, height: float) -> float:
    """
    计算BMI值（不考虑年龄和性别）（推荐：只需要BMI数值时使用）
    
    使用场景：
    - 当您只需要计算BMI数值，不需要分类评价时
    - 如果您需要同时获取BMI值和分类，请使用calculate_bmi工具
    
    Args:
        weight: 体重（公斤，数值）
        height: 身高（米，数值）
        
    Returns:
        float: BMI值（保留一位小数）
        例如: 22.9
    """
    # 参数验证
    if not isinstance(weight, (int, float)) or weight <= 0 or weight > 1000:
        raise ValueError("体重必须是0-1000之间的正数")
        
    if not isinstance(height, (int, float)) or height <= 0 or height > 3:
        raise ValueError("身高必须是0-3之间的正数（米）")
    
    # 计算BMI
    bmi = evaluator.calculate_bmi(weight, height)
    # 根据业界标准，BMI保留一位小数
    return round(bmi, 1)

@mcp.resource("bmi://standards")
def get_bmi_standards_info() -> str:
    """
    获取BMI标准信息
    
    Returns:
        str: BMI标准描述信息
    """
    info = """
    BMI标准说明：
    1. 6-17岁：按单一年龄划分，男女标准不同
    2. 18-19岁：使用同一标准，男女标准不同
    3. 20-59岁：使用同一标准，男女标准相同
    4. 60-79岁：使用同一标准，男女标准相同
    
    分类标准：
    - 偏瘦：underweight
    - 正常：normal
    - 超重：overweight
    - 肥胖：obese
    """
    return info.strip()

if __name__ == "__main__":
    # 运行MCP服务，使用STDIO方式
    mcp.run(transport="stdio")