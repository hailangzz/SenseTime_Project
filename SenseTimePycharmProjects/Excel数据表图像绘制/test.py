import pandas as pd
import matplotlib.pyplot as plt

# 创建一个示例DataFrame
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Value': [10, 20, 30, 40]
})

# 假设我们需要绘制第一行和第二行的饼图
row1 = df.iloc[0]
row2 = df.iloc[1]

# 将两行合并为一个Series
data = pd.concat([row1, row2], axis=0)
# data.index = ['Category ' + str(i) for i in range(1, 3)]  # 重新命名索引

# 绘制饼图
data.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Pie Chart of Row 1 and Row 2')
plt.axis('equal')  # 确保饼图为正圆形
plt.show()