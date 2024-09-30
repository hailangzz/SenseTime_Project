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
import yaml
import subprocess

class CreateFileDataList:
    def __init__(self, folder_path,creat_datalist_config,search_data_project_info):
        self.folder_path = folder_path
        self.creat_datalist_config = creat_datalist_config
        self.search_data_project_info = {                            #存储datalist输出名称，及标注数据项关模型项目名称的字典变量
                                "datetime_sting":"20240529_20240615",
                                "collect_cars_name": "CN-003",
                                "model_project_name":"tlr",          # 筛选对应的model项目tag真值标签数据:tlr、tsr、obstacle、animal、roadmarker
                                "frame_rate_name":"3FPS",
                                "batch_name":"b1"                    # 数据批次名称
                               }

        self.search_data_project_info=search_data_project_info

        self.file_dict = {"filename":"SDC-OSS-2_tlsr:s3://roadsemantics/TSR/20240416_H64/crop/261329/camera/00001.jpg",
                          "image_height": 792,
                          "image_width": 1408,
                          "instances": [],
                          }

        if "rear" in self.search_data_project_info["model_project_name"]:
            self.file_dict["image_height"] = 640
            self.file_dict["image_width"] = 1024

        self.file_dict_list = []

        self.search_config = {"tlr":
                                  {"tag_range_list":
                                      [ "TSLR真值-路口红绿灯",
                                        "TSLR真值-红绿灯-特殊",
                                        "TSLR真值-非行车红绿灯-单一底座提示灯",
                                        ],
                                  "camera_type_list":["center_camera_fov30","center_camera_fov120"],
                                  "interval_frame_num":3   #原始视频图像帧率为30FPS，每秒30帧。interval_frame_num=3代表每间隔3帧抽取一帧，每秒10帧。
                                  },
                              "tsr":
                                  {"tag_range_list":
                                      [
                                          "TSLR真值-限速牌",
                                          "TSLR真值-限制类标志（高宽重）",
                                          "TSLR真值-解除限速牌",
                                          "TSLR真值-解除限速类-以0结尾",
                                          "TSLR真值-限速类-以0结尾（含电子限速）",
                                          "TSLR真值-80m-TSR",
                                          "TSLR真值-限速类-以5结尾（含电子限速）",
                                          "TSLR真值-限速类-最低限速",

                                      ],
                                   "camera_type_list": ["center_camera_fov30","center_camera_fov120"],
                                   "interval_frame_num": 3
                                   # 原始视频图像帧率为30FPS，每秒30帧。interval_frame_num=3代表每间隔3帧抽取一帧，每秒10帧。
                                   },
                              "tsr_ramp":
                                  {"tag_range_list":
                                      [
                                          "TSLR真值-匝道标志"
                                      ],
                                      "camera_type_list": ["center_camera_fov30", "center_camera_fov120"],
                                      "interval_frame_num": 3
                                      # 原始视频图像帧率为30FPS，每秒30帧。interval_frame_num=3代表每间隔3帧抽取一帧，每秒10帧。
                                  },
                              "obstacle":
                                  {"tag_range_list":
                                       [
                                           "GOP真值-一般类-隔离柱",
                                           "GOP真值-一般类-护栏"
                                       ],
                                   "camera_type_list": ["center_camera_fov30","center_camera_fov120"],
                                   "interval_frame_num": 3
                                   # 原始视频图像帧率为30FPS，每秒30帧。interval_frame_num=3代表每间隔3帧抽取一帧，每秒10帧。
                                   },

                              "animal":
                                  {"tag_range_list":
                                       [
                                           "GOP真值-特定类-动物"
                                        ],
                                   "camera_type_list": ["center_camera_fov30","center_camera_fov120"],
                                   "interval_frame_num": 3
                                   # 原始视频图像帧率为30FPS，每秒30帧。interval_frame_num=3代表每间隔3帧抽取一帧，每秒10帧。
                                   },
                              "roadmarker":
                                  {"tag_range_list":
                                       [
                                           "TSLR真值-路面标识",
                                           "地面标识-多箭头类-左转掉头",
                                           "地面标识-单箭头类-掉头",
                                       ],
                                   "camera_type_list": ["center_camera_fov30","center_camera_fov120"],
                                   "interval_frame_num": 3
                                   # 原始视频图像帧率为30FPS，每秒30帧。interval_frame_num=3代表每间隔3帧抽取一帧，每秒10帧。
                                   },

                              "rear_roadmarker":
                                  {"tag_range_list":
                                      [
                                          "TSLR真值-路面标识",
                                          "地面标识-多箭头类-左转掉头",
                                          "地面标识-单箭头类-掉头",
                                      ],
                                      "camera_type_list": ["rear_camera"],
                                      "interval_frame_num": 3
                                      # 原始视频图像帧率为30FPS，每秒30帧。interval_frame_num=3代表每间隔3帧抽取一帧，每秒10帧。
                                  }
                              }

    def create_row_info_of_datalist(self):

        with open(self.folder_path, 'r', encoding='utf-8') as f:
            # 使用 json.load() 方法解析JSON文件
            data = json.load(f)
            # print(data.keys())
            for collection_type in data:
                print(collection_type)
                for monthdate in data[collection_type]:
                    print(monthdate)
                    for daytime in data[collection_type][monthdate]:
                        print(daytime)
                        for minute in data[collection_type][monthdate][daytime]:
                            print(minute)
                            for single_record_tag_info in data[collection_type][monthdate][daytime][minute]["origin_record_tag"]:
                                # print(type(single_record_tag_info["tag"]),single_record_tag_info["tag"])
                                # if "路口红绿灯" in single_record_tag_info["tag"]:
                                # 根据model项目的不同，选择对应的tag真值列表数据
                                if single_record_tag_info["tag"] in self.search_config[self.search_data_project_info["model_project_name"]]["tag_range_list"]:
                                # if "隔离柱"  in single_record_tag_info["tag"] or "护栏"  in single_record_tag_info["tag"]:
                                # if "GOP真值-特定类-动物" in single_record_tag_info["tag"]:
                                    #for camera_type in ["center_camera_fov30","center_camera_fov120","rear_camera"]:
                                # 根据model项目不同，选择对应的摄像头类型列表，不同的前视、后视摄像头
                                    for camera_type in self.search_config[self.search_data_project_info["model_project_name"]]["camera_type_list"]:
                                        bucket_path_buffer = os.path.join(collection_type,monthdate,daytime,minute,"camera",camera_type)
                                        minute_split_bucket_image_name_list = self.search_camera_frame_list(bucket_path_buffer)

                                        for camera_frame_path_index in range(len(single_record_tag_info[camera_type])):
                                            if camera_frame_path_index%self.search_config[self.search_data_project_info["model_project_name"]]["interval_frame_num"] == 0:

                                                if single_record_tag_info[camera_type][camera_frame_path_index].split("/")[-1] in minute_split_bucket_image_name_list: #如果检索出的图片索引，在桶路径下存在

                                                    file_path = os.path.join(collection_type,monthdate,daytime,minute,single_record_tag_info[camera_type][camera_frame_path_index])

                                                    self.file_dict["filename"] = (self.creat_datalist_config["Ceph Addr"] +
                                                                                  self.creat_datalist_config["Amazon S3 bucket"]+
                                                                                  self.creat_datalist_config["Project Directory"]+file_path)
                                                    # print(self.file_dict["filename"])
                                                    self.file_dict_list.append(copy.deepcopy(self.file_dict))

    def save_to_json(self, output_file):

        with open(output_file, 'w') as json_file:
            for row_dict_info in self.file_dict_list:
                json_file.write(json.dumps(row_dict_info))
                json_file.write("\n")
        json_file.close()

    def search_camera_frame_list(self,bucket_path_buffer):
        minute_split_bucket_image_name_list=[]
        calling_commands = "aws --endpoint-url=" + self.creat_datalist_config["endpoint-url"]
        profile_parameter = "--profile " + self.creat_datalist_config["Ceph Addr"].split(":")[0]
        cmd_type = "s3 ls"
        read_bucket_path = self.creat_datalist_config["Amazon S3 bucket"] +self.creat_datalist_config["Project Directory"]+ bucket_path_buffer+"/"

        command = " ".join([calling_commands, profile_parameter, cmd_type, read_bucket_path])
        # print(command)
        # result_row_info = " ".join([self.creat_datalist_config[""]])
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # 解析bucket桶中存储的图片数据：

        for row_image_name_info in result.stdout.splitlines():
            # print(row_image_name_info.split(" ")[-1])# 存储在桶路径下的图片名称
            minute_split_bucket_image_name_list.append(row_image_name_info.split(" ")[-1])

        return minute_split_bucket_image_name_list


# 用法示例
if __name__ == "__main__":
    #folder_path = '/data/TSR/S1_snap'  # 替换为要遍历的文件夹路径

    model_project_name = "rear_roadmarker" # 数据对应的模型名称：tlr、tsr、obstacle、animal、roadmarker、rear_roadmarker,tsr_ramp

    # folder_path = '/data/data_senseauto/bucket_tag_data/save_statistics_tags_info/'+model_project_name+'/2024_09/detail_tag_result_dict.json'
    folder_path = '/data/data_senseauto/bucket_tag_data/save_statistics_tags_info/' + "roadmarker" + '/2024_09/detail_tag_result_dict.json'
    search_data_project_info = {
                                "datetime_sting":"Generalization_rear_roadmarker_L_turn_and_L_U_turn_20240901_20240930",
                                "collect_cars_name": "CN-008",
                                "model_project_name":model_project_name,          # 筛选对应的model项目tag真值标签数据:tlr、tsr、obstacle、animal、roadmarker、tsr_ramp
                                "frame_rate_name":"10FPS",
                                "batch_name":"b1"
                               }
    #output_json_file = 'Generalization_L3_list.json'  # JSON 字典文件的输出路径
    # output_json_file = '20240529_20240615_CN-003_tlr.json'  # JSON 字典文件的输出路径
    # output_json_file = '20240529_20240615_CN-003_animal.json'  # JSON 字典文件的输出路径
    # output_json_file = 'Generalization_G5_obstacle_list.json'  # JSON 字典文件的输出路径

    output_json_file = folder_path.split("detail_tag_result_dict.json")[0]+"_".join(search_data_project_info.values())+".json"  # JSON 字典文件的输出路径

    data_batch_id = "Data_Collection/GT_data/hadGtParser/"
    creat_datalist_config = {
                             "endpoint-url":"http://auto-oss.iagproxy.senseauto.com",
                             "Ceph Addr":"ad_system_common:",
                             # "Ceph Addr":"SDC-OSS-3:",
                             "Amazon S3 bucket":"s3://sdc3-faw-2/",
                             "Project Directory":"HAD/"+data_batch_id
                             }

    file_lister = CreateFileDataList(folder_path,creat_datalist_config,search_data_project_info)
    file_lister.create_row_info_of_datalist()
    file_lister.save_to_json(output_json_file)


