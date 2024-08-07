import json
import os.path
#
# # 打开JSON文件
# data_tag_info = "/data/data_senseauto/bucket_tag_data/2024_05/2024_05_29/2024_05_29_11_06_35_parser/data-tag.json"
#
#
# def read_data_tag_json_info():
#     single_origin_record_tag_dict={"custom_labels":'晴天，进隧道',
#                           "tag":'车道线真值-隧道',
#                           "start":1716952055,
#                           "end":1716952115}
#     with open(data_tag_info, 'r', encoding='utf-8') as f:
#         # 使用 json.load() 方法解析JSON文件
#         data = json.load(f)
#         for tag_name in single_origin_record_tag_dict:
#
#             single_origin_record_tag_dict[tag_name] = data['origin_record_tag'][0][tag_name]
#
#         print(single_origin_record_tag_dict)
#
#
# save_camera_frame_parser_info_directory = "/data/data_senseauto/bucket_tag_data/2024_05/2024_05_29/2024_05_29_11_06_35_parser"
# def read_camera_frame_parser_name_info(camera_frame_name_file_list=["center_camera_fov30.txt","center_camera_fov120.txt","rear_camera.txt"]):
#     for camera_frame_parser_file_name in camera_frame_name_file_list:
#         camera_frame_parser_file_path = os.path.join(save_camera_frame_parser_info_directory,camera_frame_parser_file_name)
#         with open(camera_frame_parser_file_path,'r',encoding='utf-8') as f:
#             for row_camera_frame_parser_info in f.readlines():
#                 single_row_frame_info_list = [int(value) for value in row_camera_frame_parser_info.strip().split(', ')]
#                 print(row_camera_frame_parser_info.strip().split(', '))
#                 print(single_row_frame_info_list)
#
#
#     pass
#
# read_data_tag_json_info()
# read_camera_frame_parser_name_info()


# list = ["1","2","3","4"]
#
# for i_index in range(len(list)-1):
#     print(len(list))
#     print(list[i_index])
#
# index = list.index("5")
# print(index)

# import pandas as pd
#
# # 示例数据
# data = {
#     '疼痛类型': ['分娩疼痛', '肾结石', '急性胰腺炎', '三叉神经痛', '烧伤'],
#     '疼痛等级': [9, 8, 7, 10, 9]
# }
#
# # 将字典数据转换为DataFrame
# df = pd.DataFrame(data)
#
# # 输出表格到控制台
# print(df)
#
# # 保存表格为CSV文件
# df.to_csv('疼痛等级表.csv', index=False, encoding='utf-8')
#
# # 保存表格为Excel文件
# df.to_excel('疼痛等级表.xlsx', index=False, encoding='utf-8')


from datetime import datetime, timedelta


# def init_search_datetime_monthdate_and_daytime_info():
#     interval_day = 1  # 天数间隔
#     # 定义日期时间字符串的格式
#     date_format = "%Y_%m_%d"
#     # 使用 strptime 将字符串转换为 datetime 对象
#     start_date_obj = datetime.strptime("2024_06_01", date_format)
#     end_date_obj = datetime.strptime("2024_07_15", date_format)
#
#     # 生成在开始和截止日期时间之间的连续日期时间
#     current_datetime = start_date_obj
#     datetimes_list = []
#     while current_datetime <= end_date_obj:
#         string_datetime = current_datetime.strftime(date_format)
#         datetimes_list.append(string_datetime)
#         current_datetime += timedelta(days=interval_day)
#         monthdate_string = string_datetime[:7]
#         print(monthdate_string)
#     print(datetimes_list)
# init_search_datetime_monthdate_and_daytime_info()


search_data_project_info = {
    "datetime_sting": "20240529_20240615",
    "collect_cars_name": "CN-003",
    "model_project_name": "tlr",  # 筛选对应的model项目tag真值标签数据
    "frame_rate_name": "3FPS"
}
# output_json_file = 'Generalization_L3_list.json'  # JSON 字典文件的输出路径
# output_json_file = '20240529_20240615_CN-003_tlr.json'  # JSON 字典文件的输出路径
# output_json_file = '20240529_20240615_CN-003_animal.json'  # JSON 字典文件的输出路径
# output_json_file = 'Generalization_G5_obstacle_list.json'  # JSON 字典文件的输出路径
output_json_file = "_".join(search_data_project_info.values())  # JSON 字典文件的输出路径

print(output_json_file)