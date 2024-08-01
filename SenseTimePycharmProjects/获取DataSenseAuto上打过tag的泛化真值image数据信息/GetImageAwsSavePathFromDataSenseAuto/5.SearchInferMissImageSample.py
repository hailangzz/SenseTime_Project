import os
import json
import copy
class SearchInferMissImage:

    def __init__(self, origin_infer_datalist_file,check_results_detector_target_file):
        self.bucket_cloud_director = "autolabel_sdcoss3:s3://sdc3_faw/HAD/Data_Collection/GT_data/hadGtParser/HAD_gt_2dRoadSemantic/"
        self.origin_infer_datalist_file = origin_infer_datalist_file
        self.check_results_detector_target_file = check_results_detector_target_file

        self.origin_infer_datalist_ducket_path_info_dict={}
        self.check_results_detector_info_dict = {}
        self.miss_image_target_info_dict = {}
        self.miss_image_frame_interval = 10
        self.miss_frame_frequents_dict = {}

        self.chech_results_sample_number = 0
        self.miss_image_sample_number = 0
        self.output_infer_target_and_miss_target_datalist_path = ""
        self.output_infer_target_and_miss_target_dict_list = []

        self.creat_datalist_config = {
            "Ceph Addr": "autolabel_sdcoss3:",
            # "Ceph Addr":"SDC-OSS-3:",
            "Amazon S3 bucket": "s3://sdc3_faw/",
            "Project Directory": "HAD/" + "Data_Collection/GT_data/hadGtParser/HAD_gt_2dRoadSemantic/"
        }
        
    def read_check_results_detector_info(self):

        with open(self.check_results_detector_target_file, 'r', encoding='utf-8') as f:
            # 使用 json.load() 方法解析JSON文件
            data = json.load(f)
            for single_data in data:
                single_bucket_path = single_data["image_id"].split(self.bucket_cloud_director)[1]
                single_bucket_path_split_part_3 = single_bucket_path.split("/", 3)
                monthname, daytime, minute, part_bucket_name = single_bucket_path_split_part_3
                if monthname not in self.check_results_detector_info_dict:
                    self.check_results_detector_info_dict[monthname] = {}
                    if daytime not in self.check_results_detector_info_dict[monthname]:
                        self.check_results_detector_info_dict[monthname][daytime] = {}
                        if minute not in self.check_results_detector_info_dict[monthname][daytime]:
                            self.check_results_detector_info_dict[monthname][daytime][minute] = []
                            self.check_results_detector_info_dict[monthname][daytime][minute].append(
                                copy.deepcopy(part_bucket_name))
                        else:
                            if part_bucket_name not in self.check_results_detector_info_dict[monthname][daytime][minute]:
                                self.check_results_detector_info_dict[monthname][daytime][minute].append(
                                    copy.deepcopy(part_bucket_name))
                    else:
                        if minute not in self.check_results_detector_info_dict[monthname][daytime]:
                            self.check_results_detector_info_dict[monthname][daytime][minute] = []
                            self.check_results_detector_info_dict[monthname][daytime][minute].append(
                                copy.deepcopy(part_bucket_name))
                        else:
                            if part_bucket_name not in self.check_results_detector_info_dict[monthname][daytime][minute]:
                                self.check_results_detector_info_dict[monthname][daytime][minute].append(
                                    copy.deepcopy(part_bucket_name))
                else:
                    if daytime not in self.check_results_detector_info_dict[monthname]:
                        self.check_results_detector_info_dict[monthname][daytime] = {}
                        if minute not in self.check_results_detector_info_dict[monthname][daytime]:
                            self.check_results_detector_info_dict[monthname][daytime][minute] = []
                            self.check_results_detector_info_dict[monthname][daytime][minute].append(
                                copy.deepcopy(part_bucket_name))
                        else:
                            if part_bucket_name not in self.check_results_detector_info_dict[monthname][daytime][minute]:
                                self.check_results_detector_info_dict[monthname][daytime][minute].append(
                                    copy.deepcopy(part_bucket_name))
                    else:
                        if minute not in self.check_results_detector_info_dict[monthname][daytime]:
                            self.check_results_detector_info_dict[monthname][daytime][minute] = []
                            self.check_results_detector_info_dict[monthname][daytime][minute].append(
                                copy.deepcopy(part_bucket_name))
                        else:
                            if part_bucket_name not in self.check_results_detector_info_dict[monthname][daytime][minute]:
                                self.check_results_detector_info_dict[monthname][daytime][minute].append(
                                    copy.deepcopy(part_bucket_name))
                # print(monthname, daytime, minute,
                #       self.check_results_detector_info_dict[monthname][daytime][minute][-1])

    def read_origin_infer_datalist(self):
        with open(self.origin_infer_datalist_file, 'r', encoding='utf-8') as f:
            all_datalist_info = f.readlines()
            for single_datalist in all_datalist_info:
                single_data = json.loads(single_datalist)
                single_bucket_path = single_data["filename"].split(self.bucket_cloud_director)[1]
                single_bucket_path_split_part_3 = single_bucket_path.split("/",3)
                monthname,daytime,minute,part_bucket_name = single_bucket_path_split_part_3
                if monthname not in self.origin_infer_datalist_ducket_path_info_dict:
                    self.origin_infer_datalist_ducket_path_info_dict[monthname] = {}
                    if daytime not in self.origin_infer_datalist_ducket_path_info_dict[monthname]:
                        self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime]={}
                        if minute not in self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime]:
                            self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime][minute] = []
                            self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime][minute].append(part_bucket_name)
                        else:
                            self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime][minute].append(
                                copy.deepcopy(part_bucket_name))
                    else:
                        if minute not in self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime]:
                            self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime][minute] = []
                            self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime][minute].append(part_bucket_name)
                        else:
                            self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime][minute].append(
                                copy.deepcopy(part_bucket_name))
                else:
                    if daytime not in self.origin_infer_datalist_ducket_path_info_dict[monthname]:
                        self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime]={}
                        if minute not in self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime]:
                            self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime][minute] = []
                            self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime][minute].append(part_bucket_name)
                        else:
                            self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime][minute].append(
                                copy.deepcopy(part_bucket_name))
                    else:
                        if minute not in self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime]:
                            self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime][minute] = []
                            self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime][minute].append(part_bucket_name)
                        else:
                            self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime][minute].append(
                                copy.deepcopy(part_bucket_name))
                # print(single_bucket_path,monthname,daytime,minute,self.origin_infer_datalist_ducket_path_info_dict[monthname][daytime][minute][-1])
                # print(single_datalist.split("\", \"")[0])

    def find_miss_target_image(self):
        for monthday in self.check_results_detector_info_dict:
            if monthday not in self.miss_image_target_info_dict:
                self.miss_image_target_info_dict[monthday]={}
            for daytime in self.check_results_detector_info_dict[monthday]:
                if daytime not in self.miss_image_target_info_dict[monthday]:
                    self.miss_image_target_info_dict[monthday][daytime] = {}
                for minute in self.check_results_detector_info_dict[monthday][daytime]:

                    #对check_results做排序处理
                    self.check_results_detector_info_dict[monthday][daytime][minute] = sorted(self.check_results_detector_info_dict[monthday][daytime][minute])
                    self.origin_infer_datalist_ducket_path_info_dict[monthday][daytime][minute] = sorted(self.origin_infer_datalist_ducket_path_info_dict[monthday][daytime][minute])
                    if minute not in self.miss_image_target_info_dict[monthday][daytime]:
                        self.miss_image_target_info_dict[monthday][daytime][minute] = []
                    for bucker_name_index in range(len(self.check_results_detector_info_dict[monthday][daytime][minute])-1):
                        # if self.check_results_detector_info_dict[monthday][daytime][minute][bucker_name_index] == self.check_results_detector_info_dict[monthday][daytime][minute][bucker_name_index+1]:
                        #     print(monthday,daytime,minute,self.check_results_detector_info_dict[monthday][daytime][minute][bucker_name_index])

                        if "rear_camera" not in self.check_results_detector_info_dict[monthday][daytime][minute][bucker_name_index]: # 不检索后视摄像头的图像（后视中“动物”目标很少，增加后会引入大量无效数据，因此直接去除）
                            start_target_index = self.origin_infer_datalist_ducket_path_info_dict[monthday][daytime][minute].index(self.check_results_detector_info_dict[monthday][daytime][minute][bucker_name_index])
                            end_target_index = self.origin_infer_datalist_ducket_path_info_dict[monthday][daytime][minute].index(self.check_results_detector_info_dict[monthday][daytime][minute][bucker_name_index+1])

                            if end_target_index-start_target_index not in self.miss_frame_frequents_dict:
                                self.miss_frame_frequents_dict[end_target_index-start_target_index] = 1
                            else:
                                self.miss_frame_frequents_dict[end_target_index - start_target_index] += 1
                            # print(end_target_index-start_target_index)
                            if (end_target_index - start_target_index<=self.miss_image_frame_interval) and (end_target_index - start_target_index>1):
                                # print(self.check_results_detector_info_dict[monthday][daytime][minute][bucker_name_index])
                                # print(self.check_results_detector_info_dict[monthday][daytime][minute][bucker_name_index + 1])

                                for index in range(1,end_target_index-start_target_index):
                                    self.miss_image_target_info_dict[monthday][daytime][minute].append(self.origin_infer_datalist_ducket_path_info_dict[monthday][daytime][minute][start_target_index+index])
                                    print(monthday,daytime,minute,self.origin_infer_datalist_ducket_path_info_dict[monthday][daytime][minute][start_target_index+index])
                    # print("chek_resulte:",len(self.check_results_detector_info_dict[monthday][daytime][minute]),len(set(self.check_results_detector_info_dict[monthday][daytime][minute])))
                    # print(len(self.miss_image_target_info_dict[monthday][daytime][minute]),len(set(self.miss_image_target_info_dict[monthday][daytime][minute])))
    def create_infer_target_and_miss_target_datalist(self,output_infer_target_and_miss_target_datalist_path):
        # 将推理后符合阈值条件的目标样本，及其窗口内符合条件的样本整理成datalist文件。（此样本相对较准确）
        self.output_infer_target_and_miss_target_datalist_path = output_infer_target_and_miss_target_datalist_path

        single_datalist_file_dict = {"filename": "SDC-OSS-2_tlsr:s3://roadsemantics/TSR/20240416_H64/crop/261329/camera/00001.jpg",
                          "image_height": 2160,
                          "image_width": 3840,
                          "instances": [],
                          }

        for monthdate in self.check_results_detector_info_dict:
            for daytime in self.check_results_detector_info_dict[monthdate]:
                for minute in self.check_results_detector_info_dict[monthdate][daytime]:

                    check_results_list = self.check_results_detector_info_dict[monthdate][daytime][minute]
                    miss_image_target_list = self.miss_image_target_info_dict[monthdate][daytime][minute]
                    self.chech_results_sample_number += len(check_results_list)
                    self.miss_image_sample_number += len(miss_image_target_list)

                    combin_target_list = sorted(check_results_list+miss_image_target_list)
                    for single_bucket_image_path in combin_target_list:
                        file_path = os.path.join(monthdate, daytime, minute, single_bucket_image_path)

                        single_datalist_file_dict["filename"] = (self.creat_datalist_config["Ceph Addr"] +
                                                                      self.creat_datalist_config["Amazon S3 bucket"]+
                                                                      self.creat_datalist_config["Project Directory"]+file_path)
                        # print(file_path)
                        self.output_infer_target_and_miss_target_dict_list.append(copy.deepcopy(single_datalist_file_dict))


        with open(self.output_infer_target_and_miss_target_datalist_path, 'w') as json_file:
            for row_dict_info in self.output_infer_target_and_miss_target_dict_list:
                json_file.write(json.dumps(row_dict_info))
                json_file.write("\n")
        json_file.close()
        print("推理筛选数据帧后datalist样本数量：%d" % self.chech_results_sample_number)
        print("检索丢失数据帧datalist样本数量：%d" % self.miss_image_sample_number)
        print("增加推理丢失数据帧后datalist样本数量：%d"%len(self.output_infer_target_and_miss_target_dict_list))

if __name__ == "__main__":
    origin_infer_datalist_file = "Generalization_G5_animal_list.json"
    check_results_detector_target_file = "check_results.txt"
    output_infer_target_and_miss_target_datalist_path = "animal_infer_target_and_miss_target_list.json"

    search_miss_image = SearchInferMissImage(origin_infer_datalist_file,check_results_detector_target_file)
    search_miss_image.read_origin_infer_datalist()
    search_miss_image.read_check_results_detector_info()
    search_miss_image.find_miss_target_image()

    # 检索推理、阈值筛选后，丢失的数据帧频数情况。
    sorted_items = sorted(search_miss_image.miss_frame_frequents_dict.items(), key=lambda x: x[1], reverse=True)
    for key, value in sorted_items:
        print(f"{key}: {value}")

    search_miss_image.create_infer_target_and_miss_target_datalist(output_infer_target_and_miss_target_datalist_path)



