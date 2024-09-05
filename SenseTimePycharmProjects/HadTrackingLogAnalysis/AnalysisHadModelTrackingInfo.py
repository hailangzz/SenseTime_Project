import copy
import os
from datetime import datetime
import numpy as np

class AnalysisDetectBoxInfo:

    def __init__(self,total_standard_detect_target_info_list):
        self.filter_iou_threshold_dict = {"single_frame_iou_threshold": 0.8,
                                          "multi_frame_iou_threshold": 0.4}

        self.total_one_image_single_target_multi_detect_result = {"total_one_image_iou_matrix_list": [],
                                                                  "total_exist_one_image_multi_detect_index_list":[]}
        self.exist_single_target_multi_detect_image_info_dict = {"image_index":0,
                                                                 "multi_detect_box_index_list":[]}
        self.total_standard_detect_target_info_list = total_standard_detect_target_info_list
        self.analysis_one_image_single_target_multi_detect()
        self.get_total_one_image_iou_matrix_list()

        pass

    def calculate_iou(self,box1={"x1":0,"y1":0,"x2":0,"y2":0},box2={"x1":0,"y1":0,"x2":0,"y2":0}):
        # 获取边界框的左上角和右下角坐标
        b1_x1, b1_y1 = box1["x1"], box1["y1"]
        b1_x2, b1_y2 = box1["x2"], box1["y2"]
        b2_x1, b2_y1 = box2["x1"], box2["y1"]
        b2_x2, b2_y2 = box2["x2"], box2["y2"]


        # 计算面积
        area1 = (b1_x2 - b1_x1) * (b1_y2 - b1_y1)
        area2 = (b2_x2 - b2_x1) * (b2_y2 - b2_y1)

        # 计算交集的宽高
        inter_w = min(b1_x2, b2_x2) - max(b1_x1, b2_x1)
        inter_h = min(b1_y2, b2_y2) - max(b1_y1, b2_y1)

        # 如果没有交集，则IOU为0
        if inter_w <= 0 or inter_h <= 0:
            return 0.0

        # 计算交集面积
        inter_area = inter_w * inter_h
        # 计算IOU
        iou = inter_area / (area1 + area2 - inter_area)
        return iou

    def calculate_iou_matrix(self,boxes):
        """计算给定box集合中所有box的IOU矩阵"""
        iou_matrix = np.zeros((len(boxes), len(boxes)), dtype=np.float32)
        for i in range(len(boxes)):
            for j in range(i+1, len(boxes)):
                iou_matrix[i, j] = self.calculate_iou(boxes[i]["Det_Box"], boxes[j]["Det_Box"])
                # iou_matrix[j, i] = iou_matrix[i, j]  # 设置为对称矩阵
        return iou_matrix

    def get_total_one_image_iou_matrix_list(self):
        for one_image_detect_box_iou_matrix_index in range(len(self.total_one_image_single_target_multi_detect_result["total_one_image_iou_matrix_list"])):
            self.exist_single_target_multi_detect_image_info_dict = {"image_index": 0,
                                                                     "multi_detect_box_index_list": []}
            one_image_detect_box_iou_matrix = self.total_one_image_single_target_multi_detect_result["total_one_image_iou_matrix_list"][one_image_detect_box_iou_matrix_index]

            iou_filter_result = np.where(one_image_detect_box_iou_matrix>self.filter_iou_threshold_dict["single_frame_iou_threshold"])

            if len(iou_filter_result[0]>0): #如果单张图片中存在单目标多检的情况
                # print(one_image_detect_box_iou_matrix)
                # print(iou_filter_result)
                # self.self.total_one_image_single_target_multi_detect_result["total_exist_one_image_multi_detect_index_list"].append()
                self.exist_single_target_multi_detect_image_info_dict["image_index"] = one_image_detect_box_iou_matrix_index
                for iou_filter_result_number_index in range(len(iou_filter_result[0])):
                    self.exist_single_target_multi_detect_image_info_dict["multi_detect_box_index_list"].append([iou_filter_result[0][iou_filter_result_number_index],iou_filter_result[1][iou_filter_result_number_index]])

                print(self.exist_single_target_multi_detect_image_info_dict)

            # if len(iou_filter_result)>2:
            #     print(iou_filter_result,one_image_detect_box_iou_matrix)
            # pass



    def analysis_one_image_single_target_multi_detect(self):
        for detect_one_image_detect_box_result in self.total_standard_detect_target_info_list:
            iou_matrix = self.calculate_iou_matrix(detect_one_image_detect_box_result)
            self.total_one_image_single_target_multi_detect_result["total_one_image_iou_matrix_list"].append(copy.deepcopy(iou_matrix))

        # print(len(self.total_standard_detect_target_info_list))
        # print(len(self.total_one_image_single_target_multi_detect_result["total_one_image_iou_matrix_list"]))



class AnalysisHadTrackingLogInfo:
    def __init__(self,j5_perception_result_log_path="/home/SENSETIME/zhangzhuo/j5_aplog/aplog/VPER_1_19700101-200152.log"):
        self.j5_perception_result_log_path = j5_perception_result_log_path
        self.j5_log_info_result_dict= {"datetime_list":[],
                                       "total_row_info_list":[],
                                       "total_detect_target_info_list":[],
                                       "total_detect_Det_Idx_index_list":[],
                                       "total_standard_detect_target_info_list":[]}
        self.detect_result_dict={
                                 "Det_Idx":0,
                                 "Det_Category":0,
                                 "Det Score": 0,
                                 "Det_Box": {"x1":0,
                                             "y1":0,
                                             "x2":0,
                                             "y2":0}
                                }


    def standard_log_info(self,all_info_of_perception_result):
        for single_row_info_index in range(0, len(all_info_of_perception_result)):
            if "[TlsrTrackingOP] [TLSR Camera objects]: Det_Idx | Det_Category |" not in all_info_of_perception_result[single_row_info_index]:
                if " ===================================>" in all_info_of_perception_result[single_row_info_index]:
                    continue
                else:
                    self.j5_log_info_result_dict["total_row_info_list"].append(all_info_of_perception_result[single_row_info_index])
            else:
                self.j5_log_info_result_dict["total_row_info_list"].append(
                    all_info_of_perception_result[single_row_info_index].strip()+all_info_of_perception_result[single_row_info_index+1])


    def get_datetime_list_info_of_log(self,single_row_log):
        datetime_string = single_row_log.split('  ')[0]
        self.j5_log_info_result_dict["datetime_list"].append(datetime_string[:19])

        '''
        dt_obj = datetime.strptime(datetime_string, "%Y/%m/%d %H:%M:%S.%f")
        # 获取时间戳（这实际上已经包含了微秒的信息，因为timestamp()返回的是浮点数）
        timestamp = dt_obj.timestamp()
        # 打印结果
        print(timestamp)
        # 如果你需要更明确地处理微秒部分（比如转换为毫秒等），你可以这样做：
        # 获取整数秒和微秒部分
        seconds = int(timestamp)
        microseconds = int((timestamp - seconds) * 1e6)
        # print(f"Seconds: {seconds}")
        # 打印秒和微秒
        # print(f"Seconds: {seconds}, Microseconds: {microseconds}")
        '''
    def get_detect_target_result_info(self,single_row_log):

        if "[TLSR Camera objects]: Det_Idx | Det_Category | Det Score | Det_Box" in single_row_log:
            detect_result_info_string = single_row_log.split("===================================> ")[-1][:-2]
            detect_result_info_list = detect_result_info_string.split(" | ")

            self.detect_result_dict["Det_Idx"] = detect_result_info_list[0]
            self.detect_result_dict["Det_Category"] = detect_result_info_list[1]
            self.detect_result_dict["Det Score"] = float(detect_result_info_list[2])

            box_of_result_info = eval(detect_result_info_list[3])
            self.detect_result_dict["Det_Box"]['x1'] = box_of_result_info[0]
            self.detect_result_dict["Det_Box"]['y1'] = box_of_result_info[1]
            self.detect_result_dict["Det_Box"]['x2'] = box_of_result_info[2]
            self.detect_result_dict["Det_Box"]['y2'] = box_of_result_info[3]
            # print(self.detect_result_dict)

            self.j5_log_info_result_dict["total_detect_target_info_list"].append(copy.deepcopy(self.detect_result_dict))

    def get_total_detect_Det_Idx_index_list(self):
        total_detect_Det_Idx_list = []
        for single_detect_perecption_result in self.j5_log_info_result_dict["total_detect_target_info_list"]:
            total_detect_Det_Idx_list.append(single_detect_perecption_result["Det_Idx"])
        self.j5_log_info_result_dict["total_detect_Det_Idx_index_list"] = indexes_of_three = [i for i, val in enumerate(total_detect_Det_Idx_list) if val == "0"]
        # print(total_detect_Det_Idx_list)
        # print(self.j5_log_info_result_dict["total_detect_Det_Idx_index_list"])
        for index in range(0,len(self.j5_log_info_result_dict["total_detect_Det_Idx_index_list"])-1):
            single_image_detect_box_info_start_index = self.j5_log_info_result_dict["total_detect_Det_Idx_index_list"][index]
            single_image_detect_box_info_end_index = self.j5_log_info_result_dict["total_detect_Det_Idx_index_list"][index+1]
            single_image_detect_result_list = []
            for detect_result_index in range(single_image_detect_box_info_start_index,single_image_detect_box_info_end_index):
                single_image_detect_result_list.append(self.j5_log_info_result_dict["total_detect_target_info_list"][detect_result_index])
            # 此处未解析最后一帧图像的预测结果列表
            self.j5_log_info_result_dict["total_standard_detect_target_info_list"].append(copy.deepcopy(single_image_detect_result_list))
        # print(self.j5_log_info_result_dict["total_standard_detect_target_info_list"],len(self.j5_log_info_result_dict["total_standard_detect_target_info_list"]))

    def read_j5_perception_result_log_info(self):

        with open(self.j5_perception_result_log_path,"r") as j5_perception_log_cur:
            all_info_of_perception_result = j5_perception_log_cur.readlines()
            self.standard_log_info(all_info_of_perception_result)
            for single_row_log in self.j5_log_info_result_dict["total_row_info_list"]:
                self.get_datetime_list_info_of_log(single_row_log)
                self.get_detect_target_result_info(single_row_log)

        self.get_total_detect_Det_Idx_index_list()





analysis_tracking_info = AnalysisHadTrackingLogInfo()
analysis_tracking_info.read_j5_perception_result_log_info()

analysis_detect_box_info = AnalysisDetectBoxInfo(analysis_tracking_info.j5_log_info_result_dict["total_standard_detect_target_info_list"])