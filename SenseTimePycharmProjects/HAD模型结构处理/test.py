import torch
import torch.nn as nn


# 假设你的模型类名为MyModel
class MyModel(nn.Module):
    # 定义你的模型结构
    pass


# 实例化模型
model = MyModel()

# 加载模型权重
model.load_state_dict(torch.load('your_model.pth'))

# 确保模型在评估模式
model.eval()