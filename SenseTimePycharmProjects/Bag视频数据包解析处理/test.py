import datetime

# 输入的日期时间字符串
date_string = "2023-12-14-11-44-32"

# 定义日期时间字符串的格式
date_format = "%Y-%m-%d-%H-%M-%S"

# 将字符串转换为datetime对象
date_time_obj = datetime.datetime.strptime(date_string, date_format)
time_delta = datetime.timedelta(hours=8)
new_date_time_obj = date_time_obj + time_delta
print(date_time_obj)
print(str(int(new_date_time_obj.timestamp())))
# 打印转换后的datetime
