import json
import os

class BMIEvaluator:
    def __init__(self):
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建标准文件路径
        standards_file = os.path.join(current_dir, 'bmi_standards.json')
        
        # 读取标准数据
        with open(standards_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.standards = data['bmi_standards']
    
    def calculate_bmi(self, weight, height):
        """
        计算BMI值
        
        Args:
            weight: 体重(公斤)
            height: 身高(米)
            
        Returns:
            BMI值
        """
        bmi = weight / (height ** 2)
        # 根据业界标准，BMI保留一位小数
        return round(bmi, 1)
    
    def get_bmi_category(self, age, gender, bmi):
        """
        根据年龄、性别和BMI值获取分类
        
        Args:
            age: 年龄
            gender: 性别('male'或'female')
            bmi: BMI值
            
        Returns:
            分类结果
        """
        # 确定年龄组
        if 6 <= age <= 17:
            age_group = str(age)
        elif 18 <= age <= 19:
            age_group = "18-19"
        elif 20 <= age <= 59:
            # 成年人使用统一标准
            age_group = "20-59"
        elif 60 <= age <= 79:
            # 老年人使用统一标准
            age_group = "60-79"
        else:
            raise ValueError("年龄必须在6-79岁之间")
        
        # 获取对应年龄组和性别的标准
        if gender in self.standards and age_group in self.standards[gender]:
            standards = self.standards[gender][age_group]
        else:
            raise ValueError(f"未找到年龄组{age_group}和性别{gender}的标准")
        
        # 根据BMI值判断分类
        # 标准数据格式: {"underweight": [0, 18.4], "normal": [18.5, 23.9], ...}
        if bmi <= standards["underweight"][1]:  # <= 上限值
            return "underweight"
        elif bmi <= standards["normal"][1]:     # <= 上限值
            return "normal"
        elif bmi <= standards["overweight"][1]: # <= 上限值
            return "overweight"
        else:
            return "obese"
    
    def evaluate(self, age, gender, weight, height):
        """
        综合评价BMI
        
        Args:
            age: 年龄
            gender: 性别('male'或'female')
            weight: 体重(公斤)
            height: 身高(米)
            
        Returns:
            包含BMI值和分类的字典
        """
        bmi = self.calculate_bmi(weight, height)
        category = self.get_bmi_category(age, gender, bmi)
        return {
            "bmi": bmi,
            "category": category
        }