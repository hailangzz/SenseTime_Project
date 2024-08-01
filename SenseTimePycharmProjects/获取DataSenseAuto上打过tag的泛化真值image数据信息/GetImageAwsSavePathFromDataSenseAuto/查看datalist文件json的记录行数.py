import json

data_json_path = r"/home/SENSETIME/zhangzhuo/PycharmProjects/SenseTimePycharmProjects/获取DataSenseAuto上打过tag的泛化真值image数据信息/GetImageAwsSavePathFromDataSenseAuto/20240529_20240615_CN-003_tlr.json"
data_json_path_3FTP = r"/home/SENSETIME/zhangzhuo/PycharmProjects/SenseTimePycharmProjects/获取DataSenseAuto上打过tag的泛化真值image数据信息/GetImageAwsSavePathFromDataSenseAuto/20240529_20240615_CN-003_tlr_3FPS_b1.json"

with open(data_json_path, 'r', encoding='utf-8') as f:
        all_datalist_info = f.readlines()
        print(len(all_datalist_info))

with open(data_json_path_3FTP, 'r', encoding='utf-8') as f:
        all_datalist_info = f.readlines()
        print(len(all_datalist_info))