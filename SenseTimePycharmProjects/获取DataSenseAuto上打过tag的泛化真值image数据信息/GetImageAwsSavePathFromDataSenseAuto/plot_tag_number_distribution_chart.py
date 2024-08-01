import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import json

# 设置中文字体
font = FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')

# 读取tag_数据量统计
data_tag_file_path = r"statistics_tag_info_dict.json"
data_tag_info_dict = {}

with open(data_tag_file_path, 'r', encoding='utf-8') as f:
    # 使用 json.load() 方法解析JSON文件
    data_tag_info_dict = json.load(f)
print(data_tag_info_dict["tag_statistics_info"])

#计算tag总量
tag_total_number = 0
for keys_name in data_tag_info_dict["tag_statistics_info"]:
    tag_total_number+=data_tag_info_dict["tag_statistics_info"][keys_name]

# # 示例数据
# data = {
#     '分娩疼痛': 9,
#     '肾结石': 8,
#     '急性胰腺炎': 7,
#     '三叉神经痛': 10,
#     '烧伤': 9,
# }

# 提取字典中的键和值
labels = list(data_tag_info_dict["tag_statistics_info"].keys())
labels = [value.split("-",1)[1] for value in labels]

values = list(data_tag_info_dict["tag_statistics_info"].values())

# 创建条形图
plt.figure(figsize=(20, 9))
bars = plt.bar(labels, values, color='skyblue')

# 添加标题和标签
plt_title_string = "FAW-HAD真值解析数据量统计（总量：%d）" % tag_total_number
plt.title(plt_title_string, fontproperties=font)
plt.xlabel('HAD真值标签', fontproperties=font)
plt.ylabel('数量', fontproperties=font)

# 设置x轴刻度的字体属性
# plt.xticks(fontproperties=font)
plt.xticks(fontproperties=font, rotation=45)

# 在每个柱形条上添加数量标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, str(height), ha='center', va='bottom', fontproperties=font)

# 调整子图的布局
plt.tight_layout()
# 显示图形
plt.show()

#保存为表格数据
print(data_tag_info_dict["tag_statistics_info"])
import pandas as pd
#将字典数据转换为DataFrame
data_tag_info_dict["tag_statistics_info"]["总量"]=tag_total_number
df = pd.DataFrame(list(data_tag_info_dict["tag_statistics_info"].items()), columns=['FAW-HAD真值标签', '数量'])
# df = pd.DataFrame(data_tag_info_dict["tag_statistics_info"])
# 输出表格到控制台
# print(df)
# 保存表格为Excel文件
df.to_excel('FAW-HAD真值解析数据量统计表.xlsx', index=False, encoding='utf-8')
