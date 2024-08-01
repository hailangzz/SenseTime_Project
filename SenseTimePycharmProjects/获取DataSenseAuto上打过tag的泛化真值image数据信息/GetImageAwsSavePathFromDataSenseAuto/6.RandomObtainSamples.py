import os
import json
import copy
import random

class RandomObtainSample:
    def __init__(self,anno_origin_file_path=r"/data/Generalization/G5/tlr/anno",sample_target_quantity = 20000,save_filter_sample_file_path="random_filter_anno.txt"):
        self.anno_origin_file_path = anno_origin_file_path
        self.sample_target_quantity = sample_target_quantity
        self.save_filter_sample_file_path = save_filter_sample_file_path

        self.origin_annotation_file_name = "final_anno.txt"
        self.total_origin_sample_path_info_dict = {}
        self.video_sample_clip_minute_list = []
        self.filter_datalist_sample=[] #筛选出的样本路径列表

    def get_random_annotation_datalist(self):
        origin_annotation_file_path = os.path.join(self.anno_origin_file_path,self.origin_annotation_file_name)
        with open(origin_annotation_file_path, 'r', encoding='utf-8') as f:
            # 使用 json.load() 方法解析JSON文件
            all_datalist = f.readlines()
            for single_sample_path in all_datalist:
                clip_minute_name = single_sample_path.split("/")[2]

                if clip_minute_name not in self.total_origin_sample_path_info_dict:
                    self.video_sample_clip_minute_list.append(clip_minute_name)
                    self.total_origin_sample_path_info_dict[clip_minute_name] = []

                self.total_origin_sample_path_info_dict[clip_minute_name].append(single_sample_path)


        # print(self.video_sample_clip_minute_list)
        # 打乱复制后的数组
        random.shuffle(self.video_sample_clip_minute_list)
        # print(self.video_sample_clip_minute_list)
        #抽取指定数量的样本：
        for clip_minute_name in self.video_sample_clip_minute_list:
            for sample_path in self.total_origin_sample_path_info_dict[clip_minute_name]:
                self.filter_datalist_sample.append(sample_path)
            if len(self.filter_datalist_sample)>=self.sample_target_quantity:
                break
        # print(self.filter_datalist_sample)
        # print(len(self.filter_datalist_sample))

    def save_filter_sample_file(self):
        with open(self.save_filter_sample_file_path,'w') as f:
            for single_sample_path in self.filter_datalist_sample:
                f.write(single_sample_path)

anno_origin_file_path=r"/data/Generalization/G5/tlr/anno"
sample_target_quantity = 20000
save_filter_sample_file_path = os.path.join(anno_origin_file_path,r"random_filter_anno.txt")

random_get_annotation_sample = RandomObtainSample(anno_origin_file_path,sample_target_quantity,save_filter_sample_file_path)
random_get_annotation_sample.get_random_annotation_datalist()
random_get_annotation_sample.save_filter_sample_file()