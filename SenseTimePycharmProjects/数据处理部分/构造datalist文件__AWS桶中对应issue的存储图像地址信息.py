'''
    # 说明datalist为训练数据处理时，指定Ceph 是一种分布式存储系统节点与 Amazon S3 存储桶中存储图像路径对应关系的json表结构。
    #   示例：
    #       {"filename": "SDC-OSS-2_tlsr:s3://roadsemantics/TSR/20240416_H64/crop/261329/camera/00001.jpg", "image_height": 2160, "image_width": 3840, "instances": []}
    #   说明：
    #       SDC-OSS-2_tlsr：Ceph 存储集群中节点的地址，存储或服务器的名称
    #       s3:// ：表示 Amazon S3 存储桶中的路径
    #       roadsemantics：存储桶的名称
    #       TSR/20240416_H64/crop/261329/camera/00001.jpg：图片文件在存储桶中的键（Key），指定了文件在存储桶中的具体位置（存储路径）
'''

import os
import json
import copy

class CreateFileDataList:
    def __init__(self, folder_path,creat_datalist_config):
        self.folder_path = folder_path
        self.creat_datalist_config = creat_datalist_config

        self.file_dict = {"filename":"SDC-OSS-2_tlsr:s3://roadsemantics/TSR/20240416_H64/crop/261329/camera/00001.jpg",
                          "image_height": 2160,
                          "image_width": 3840,
                          "instances": [],
                          }
        self.file_dict_list = []

    def list_files(self):
        for root, dirs, files in os.walk(self.folder_path):
            for file_name in files:
                file_path_buff = os.path.join(root, file_name)
                file_path = file_path_buff.split(self.folder_path)[1]
                self.file_dict["filename"] = (self.creat_datalist_config["Ceph Addr"]+
                                              self.creat_datalist_config["Amazon S3 bucket"]+
                                              self.creat_datalist_config["Project Directory"]+file_path)
                print(self.file_dict["filename"])
                self.file_dict_list.append(copy.deepcopy(self.file_dict))

    def save_to_json(self, output_file):

        with open(output_file, 'w') as json_file:
            for row_dict_info in self.file_dict_list:
                json_file.write(json.dumps(row_dict_info))
                json_file.write("\n")
        json_file.close()


# 用法示例
if __name__ == "__main__":
    #folder_path = '/data/TSR/S1_snap'  # 替换为要遍历的文件夹路径
    folder_path = '/data/animal/A4_snap'
    #output_json_file = 'Generalization_L3_list.json'  # JSON 字典文件的输出路径
    output_json_file = 'animal_A4_list.json'  # JSON 字典文件的输出路径
    data_batch_id = "20240709_A4"
    creat_datalist_config = {"Ceph Addr":"sensecore-rs:",
                             "Amazon S3 bucket":"s3://roadsemantics/",
                             "Project Directory":"had/"+data_batch_id
                             }
    file_lister = CreateFileDataList(folder_path,creat_datalist_config)
    file_lister.list_files()
    file_lister.save_to_json(output_json_file)


