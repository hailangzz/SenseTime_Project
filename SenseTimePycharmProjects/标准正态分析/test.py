import scipy.stats as stats

# 定义均值和标准差
mean = 35
std_dev = 4.5

# 定义要计算概率的值
value = 38.3


# 计算累积分布函数 (CDF) 的值
probability = stats.norm.cdf(value, mean, std_dev)

print(f"累积概率为: {probability}")
