import os
import json
import copy

class SearchCameraTagFrameInfo:

    def __init__(self,config_info_dict):

        self.config_info_dict = config_info_dict
        self.origin_bucket_tag_data_path = config_info_dict["origin_bucket_tag_data_path"] #之前下载的tags info 信息文件目录，data-tags、fov120、fov30.txt文件
        self.data_tag_file_name = "data-tag.json"
        self.camera_frame_name_file_list=["center_camera_fov30", "center_camera_fov120", "rear_camera"]
        self.tags_data_collection_type_dict={}  # tags数据的采集方式

        self.single_origin_record_tag_dict = {"custom_labels": '晴天，进隧道',
                                              "tag": '车道线真值-隧道',
                                              "start": 1716952055,
                                              "end": 1716952115,
                                              "center_camera_fov30": [],
                                              "center_camera_fov120": [],
                                              "rear_camera": []
                                              }

        self.statistics_tag_info_dict={"custom_labels_statistics_info":{},
                                       "tag_statistics_info":{}}

        self.search_data_senseauto_camera_tag_dict = {}  # 筛选过真值标签的数据帧结构体

    def search_camera_frame_parser_name_info(self,data_tag_father_path,start_time=1716952055,end_time=1716952115):
        search_camera_frame_name_dict = {"center_camera_fov30": [],
                                         "center_camera_fov120": [],
                                         "rear_camera": []
                                         }

        for camera_frame_parser_file_name in self.camera_frame_name_file_list:  #读取tag标签路径下的camera帧记录文件["center_camera_fov30.txt", "center_camera_fov120.txt", "rear_camera.txt"]
            camera_frame_parser_file_path = os.path.join(data_tag_father_path,
                                                         camera_frame_parser_file_name+".txt")

            try:
                with open(camera_frame_parser_file_path, 'r', encoding='utf-8') as f:
                    for row_camera_frame_parser_info in f.readlines():
                        # single_row_frame_info_list = [int(value) for value in
                        #                               row_camera_frame_parser_info.strip().split(', ')]
                        string_single_row_frame_start_info = row_camera_frame_parser_info.strip().split(', ')[1]
                        int_single_row_frame_start_info = int(string_single_row_frame_start_info[:10])

                        if int_single_row_frame_start_info>=start_time and int_single_row_frame_start_info<=end_time:

                            search_camera_frame_bucket_path = os.path.join("camera",camera_frame_parser_file_name,string_single_row_frame_start_info+".jpg")
                            search_camera_frame_name_dict[camera_frame_parser_file_name].append(search_camera_frame_bucket_path)
            except Exception as e:
                print(e)

            self.single_origin_record_tag_dict[camera_frame_parser_file_name] = search_camera_frame_name_dict[camera_frame_parser_file_name]  # 为筛选的摄像头帧bucket存储路径赋值
            # print(self.single_origin_record_tag_dict[camera_frame_parser_file_name])
        # return search_camera_frame_name_dict

    def read_data_tag_json_info(self,data_tag_father_path):
        single_origin_record_tag_dict = {"custom_labels": '晴天，进隧道',
                                         "tag": '车道线真值-隧道',
                                         "start": 1716952055,
                                         "end": 1716952115}

        minute_origin_record_tag_dict_list = []

        data_tag_file_path = os.path.join(data_tag_father_path,self.data_tag_file_name)
        with open(data_tag_file_path, 'r', encoding='utf-8') as f:
            # 使用 json.load() 方法解析JSON文件
            data = json.load(f)
            for origin_record_tag_index in range(len(data['origin_record_tag'])): #循环每分钟视频切片的tag标签数组

                # for tag_name in single_origin_record_tag_dict:                    #获取单个tag标签数组的实际信息
                #     if tag_name!='end':
                #         single_origin_record_tag_dict[tag_name] = data['origin_record_tag'][origin_record_tag_index][tag_name]
                #         self.single_origin_record_tag_dict[tag_name] = single_origin_record_tag_dict[tag_name]
                #     else:
                #         if tag_name not in data['origin_record_tag'][origin_record_tag_index]:
                #             single_origin_record_tag_dict[tag_name] =  data['origin_record_tag'][origin_record_tag_index]['start']+2*60*1000
                #             self.single_origin_record_tag_dict[tag_name] = single_origin_record_tag_dict[tag_name]
                #         else:
                #             single_origin_record_tag_dict[tag_name] = \
                #             data['origin_record_tag'][origin_record_tag_index][tag_name]
                #             self.single_origin_record_tag_dict[tag_name] = single_origin_record_tag_dict[tag_name]

                self.single_origin_record_tag_dict["custom_labels"] = data['origin_record_tag'][origin_record_tag_index]["custom_labels"]
                self.single_origin_record_tag_dict["tag"] = data['origin_record_tag'][origin_record_tag_index]["tag"]
                # 时间戳存在位数差异，有的是10位有的是13位
                digit_count = len(str(data['origin_record_tag'][origin_record_tag_index]["start"]))
                if digit_count==10:#此时为妙级别时间戳
                    self.single_origin_record_tag_dict["start"] = data['origin_record_tag'][origin_record_tag_index]["start"]-6  # 注意此时扩大2秒的图像采集范围：
                    if 'end' in data['origin_record_tag'][origin_record_tag_index]:
                        self.single_origin_record_tag_dict["end"] = data['origin_record_tag'][origin_record_tag_index][
                            "end"]
                    else:
                        # 时间戳存在位数差异，有的是10位有的是13位
                        self.single_origin_record_tag_dict["end"] = data['origin_record_tag'][origin_record_tag_index][
                                                                        "start"] + 2 * 60
                else: #毫秒级计时时
                    self.single_origin_record_tag_dict["start"] = data['origin_record_tag'][origin_record_tag_index]["start"]/1000-6   # 注意此时扩大2秒的图像采集范围：
                    if 'end' in data['origin_record_tag'][origin_record_tag_index]:
                        self.single_origin_record_tag_dict["end"] = data['origin_record_tag'][origin_record_tag_index][
                            "end"]/1000
                    else:
                        # 时间戳存在位数差异，有的是10位有的是13位
                        self.single_origin_record_tag_dict["end"] = data['origin_record_tag'][origin_record_tag_index][
                                                                        "start"]/1000 + 2 * 60


                self.search_camera_frame_parser_name_info(data_tag_father_path,self.single_origin_record_tag_dict["start"],self.single_origin_record_tag_dict["end"])


                minute_origin_record_tag_dict_list.append(copy.deepcopy(self.single_origin_record_tag_dict))
        return minute_origin_record_tag_dict_list

    # def analysis_data_senseauto_bucket_tag_data(self):
    #
    #     for monthdate in os.listdir(self.origin_bucket_tag_data_path):
    #         if monthdate ==self.config_info_dict["search_month"]:
    #             if monthdate not in self.search_data_senseauto_camera_tag_dict:
    #                 self.search_data_senseauto_camera_tag_dict[monthdate]={}
    #             for daytime in os.listdir(os.path.join(self.origin_bucket_tag_data_path,monthdate)):
    #                 # print(daytime)
    #                 if daytime not in self.search_data_senseauto_camera_tag_dict[monthdate]:
    #                     self.search_data_senseauto_camera_tag_dict[monthdate][daytime]={}
    #                 for minute in os.listdir(os.path.join(self.origin_bucket_tag_data_path,monthdate,daytime)):
    #                     if minute not in self.search_data_senseauto_camera_tag_dict[monthdate][daytime]:
    #                         self.search_data_senseauto_camera_tag_dict[monthdate][daytime][minute]={"origin_record_tag":[]}
    #                     data_tag_father_path = os.path.join(self.origin_bucket_tag_data_path,monthdate,daytime,minute)
    #                     minute_origin_record_tag_dict_list = self.read_data_tag_json_info(data_tag_father_path)
    #                     self.search_data_senseauto_camera_tag_dict[monthdate][daytime][minute]["origin_record_tag"] = minute_origin_record_tag_dict_list
    #
    #     # 将字典保存为JSON文件
    #     with open(self.config_info_dict["save_statistics_tags_info_path"]+'detail_tag_result_dict.json', 'w', encoding='utf-8') as f:
    #         json.dump(self.search_data_senseauto_camera_tag_dict, f, ensure_ascii=False, indent=4)

    def analysis_data_senseauto_bucket_tag_data(self):
        for tags_collection_type in os.listdir(self.origin_bucket_tag_data_path):
            if tags_collection_type not in self.tags_data_collection_type_dict:
                self.tags_data_collection_type_dict[tags_collection_type]={}

            for monthdate in os.listdir(os.path.join(self.origin_bucket_tag_data_path,tags_collection_type)):
                if monthdate in self.config_info_dict["search_month"]:
                    if monthdate not in self.search_data_senseauto_camera_tag_dict:
                        self.search_data_senseauto_camera_tag_dict[monthdate]={}
                    for daytime in os.listdir(os.path.join(self.origin_bucket_tag_data_path,tags_collection_type,monthdate)):
                        # print(daytime)
                        if daytime not in self.search_data_senseauto_camera_tag_dict[monthdate]:
                            self.search_data_senseauto_camera_tag_dict[monthdate][daytime]={}
                        for minute in os.listdir(os.path.join(self.origin_bucket_tag_data_path,tags_collection_type,monthdate,daytime)):
                            if minute not in self.search_data_senseauto_camera_tag_dict[monthdate][daytime]:
                                self.search_data_senseauto_camera_tag_dict[monthdate][daytime][minute]={"origin_record_tag":[]}
                            data_tag_father_path = os.path.join(self.origin_bucket_tag_data_path,tags_collection_type,monthdate,daytime,minute)
                            minute_origin_record_tag_dict_list = self.read_data_tag_json_info(data_tag_father_path)
                            self.search_data_senseauto_camera_tag_dict[monthdate][daytime][minute]["origin_record_tag"] = minute_origin_record_tag_dict_list
            self.tags_data_collection_type_dict[tags_collection_type] = copy.deepcopy(self.search_data_senseauto_camera_tag_dict)
        # 将字典保存为JSON文件
        with open(self.config_info_dict["save_statistics_tags_info_path"]+'detail_tag_result_dict.json', 'w', encoding='utf-8') as f:
            json.dump(self.tags_data_collection_type_dict, f, ensure_ascii=False, indent=4)


    def statustucs_search_senseauto_camera_tag_number(self):
        for monthdate in self.search_data_senseauto_camera_tag_dict:
            for daytime in self.search_data_senseauto_camera_tag_dict[monthdate]:
                print(daytime)
                for minute in self.search_data_senseauto_camera_tag_dict[monthdate][daytime]:
                    for record_tag in self.search_data_senseauto_camera_tag_dict[monthdate][daytime][minute]["origin_record_tag"]:
                        # print(record_tag["custom_labels"])
                        try:
                            # print(record_tag)
                            if len(record_tag["custom_labels"])>0:
                                if record_tag["custom_labels"][0] not in self.statistics_tag_info_dict["custom_labels_statistics_info"]:
                                    self.statistics_tag_info_dict["custom_labels_statistics_info"][record_tag["custom_labels"][0]] = 1
                                else:
                                    self.statistics_tag_info_dict["custom_labels_statistics_info"][
                                        record_tag["custom_labels"][0]] += 1

                            if record_tag["tag"] not in self.statistics_tag_info_dict["tag_statistics_info"]:
                                self.statistics_tag_info_dict["tag_statistics_info"][record_tag["tag"]] = 1
                            else:
                                self.statistics_tag_info_dict["tag_statistics_info"][
                                    record_tag["tag"]] += 1
                        except Exception as e:
                            print(e)

        print(self.statistics_tag_info_dict)
        # 将字典保存为JSON文件
        with open(self.config_info_dict["save_statistics_tags_info_path"]+'statistics_tag_info_dict.json', 'w', encoding='utf-8') as f:
            print(self.config_info_dict["save_statistics_tags_info_path"]+'statistics_tag_info_dict.json')
            json.dump(self.statistics_tag_info_dict, f, ensure_ascii=False, indent=4)

config_info_dict = {
                    "origin_bucket_tag_data_path":"/data/data_senseauto/bucket_tag_data/HAD_tags_info_folder/roadmarker/202409",
                    "search_month":["2024_09","2024_08","2024_07"],
                    "save_statistics_tags_info_path":"/data/data_senseauto/bucket_tag_data/save_statistics_tags_info/roadmarker/2024_09/"
                    }

search_tag_frame_info = SearchCameraTagFrameInfo(config_info_dict)
search_tag_frame_info.analysis_data_senseauto_bucket_tag_data()
search_tag_frame_info.statustucs_search_senseauto_camera_tag_number()