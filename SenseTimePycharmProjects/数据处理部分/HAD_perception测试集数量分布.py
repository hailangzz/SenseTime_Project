import os
import json

class HadPerceptionTestSampleInfo:
    def __init__(self):
        self.pereception_model_name_list = ["tlr","tsr","obstacle","roadmarker","pole","rm_roadmarker","rm_pole","animal"]

        self.detect_classify_minimum_quantity_num = 100
        self.had_perception_info_dict={
            "total_model_classify_label_number":{
                "tlr": (1,22),
                "tsr": (1,79),
                "obstacle": (1,6),
                "roadmarker": (1,44),
                "pole": (1,1),
                "rm_roadmarker": (1,44),
                "rm_pole": (1,1),
                "animal": (0,4),
                                                },
            "total_model_test_datalist_path":{
                "tlr":"/data/data_after_annotation/tlr/Total_TLR_all_in_history/b25866_b24233_b24066_b22592_b21771_b21716_b21710_b21346_b21013_exp.json",
                "tsr":"/data/data_after_annotation/tsr/Total_TSR_all_in_history/b20240_b21345_b21704_b21774_b21777_b21971_b22593_b24067_b24253_b25926_b22630_b23602_exp.json",
                "obstacle":"/data/data_after_annotation/obstacle/Total_obstacle_all_in_history/b23759_b22590_b21757_b21715_b21711_b21347_b21015_exp.json",
                "roadmarker":"/data/data_after_annotation/roadmarker/Total_roadmarker_all_in_history/b21344_b21722_b22558_b23686_b23831_b24888_exp.json",
                "pole":"/data/data_after_annotation/pole/Total_pole_all_in_history/b23687_b21720_exp.json",
                "rm_roadmarker":"/data/data_after_annotation/rm_roadmarker/Total_rm_roadmarker_all_in_history/b24887_b23830_b21721_b21333_b21012_exp.json",
                "rm_pole":"/data/data_after_annotation/rm_pole/Total_rm_pole_all_in_history/b22563_b21707_exp.json",
                "animal":"/data/data_after_annotation/animal/Total_animal_all_in_history/b24079_b23760_b21925_exp.json"},

            "total_model_test_sample_label_classify_number":{
                                                             "tlr": {},
                                                             "tsr": {},
                                                             "obstacle": {},
                                                             "roadmarker": {},
                                                             "pole": {},
                                                             "rm_roadmarker": {},
                                                             "rm_pole": {},
                                                             "animal": {},
                                                             },

            "total_model_label_filename_dict": {
                "tlr": {},
                "tsr": {},
                "obstacle": {},
                "roadmarker": {},
                "pole": {},
                "rm_roadmarker": {},
                "rm_pole": {},
                "animal": {},
            },

            "total_model_label_classify_need_add_num": {
                "tlr": {},
                "tsr": {},
                "obstacle": {},
                "roadmarker": {},
                "pole": {},
                "rm_roadmarker": {},
                "rm_pole": {},
                "animal": {},
            }
        }




    def read_test_sample_classify_info(self):
        for model_name in self.pereception_model_name_list:

            with open(self.had_perception_info_dict["total_model_test_datalist_path"][model_name], 'r', encoding='utf-8') as f:

                all_array_info = f.readlines()
                # 使用 json.load() 方法解析JSON文件
                for array_info in all_array_info:  # 每一个图片样本的标注记录
                    result_array = json.loads(array_info)
                    # print(result_array["instances"])
                    for singel_label_info in result_array["instances"]: #每张图片标注信息的单个标注框信息
                        #print(result_array["filename"])
                        # print(singel_label_info)
                        if singel_label_info["label"] not in self.had_perception_info_dict["total_model_label_filename_dict"][model_name]:
                            self.had_perception_info_dict["total_model_label_filename_dict"][model_name][
                                singel_label_info["label"]] = []
                            # print(singel_label_info["label"])
                        #     self.had_perception_info_dict["total_model_label_filename_dict"][model_name][singel_label_info["label"]]=[]
                        if result_array["filename"] not in self.had_perception_info_dict["total_model_label_filename_dict"][model_name][singel_label_info["label"]]:
                            self.had_perception_info_dict["total_model_label_filename_dict"][model_name][
                                singel_label_info["label"]].append(result_array["filename"])




    def get_test_sample_classify_number(self):

        for model_name in self.had_perception_info_dict["total_model_label_filename_dict"]:
            # print(model_name)
            for classify_label in self.had_perception_info_dict["total_model_label_filename_dict"][model_name]:
                # print(classify_label,len(self.had_perception_info_dict["total_model_label_filename_dict"][model_name][classify_label]))
                # print(len(self.had_perception_info_dict["total_model_label_filename_dict"][model_name][classify_label]))
                if classify_label not in self.had_perception_info_dict["total_model_test_sample_label_classify_number"][model_name]:
                    self.had_perception_info_dict["total_model_test_sample_label_classify_number"][model_name][classify_label] = len(self.had_perception_info_dict["total_model_label_filename_dict"][model_name][classify_label])

        # print(self.had_perception_info_dict["total_model_test_sample_label_classify_number"])

    def calculate_label_classify_need_add_num(self):
        for model_name in self.pereception_model_name_list:
            model_label_begin = self.had_perception_info_dict["total_model_classify_label_number"][model_name][0]
            model_label_end = self.had_perception_info_dict["total_model_classify_label_number"][model_name][1]
            for model_classify_label in range(model_label_begin,model_label_end+1):

                if model_classify_label in self.had_perception_info_dict["total_model_test_sample_label_classify_number"][model_name]:
                    if self.had_perception_info_dict["total_model_test_sample_label_classify_number"][model_name][model_classify_label]>=self.detect_classify_minimum_quantity_num:
                        self.had_perception_info_dict["total_model_label_classify_need_add_num"][model_name][model_classify_label] = 0
                    else:

                        self.had_perception_info_dict["total_model_label_classify_need_add_num"][model_name][
                            model_classify_label] = self.detect_classify_minimum_quantity_num - self.had_perception_info_dict["total_model_test_sample_label_classify_number"][model_name][model_classify_label]
                else:
                    self.had_perception_info_dict["total_model_label_classify_need_add_num"][model_name][
                        model_classify_label] = self.detect_classify_minimum_quantity_num

        # print(self.had_perception_info_dict["total_model_label_classify_need_add_num"])

        # 存储数据到json文件：
        # 直接将变量存储到JSON文件
        with open('label_classify_need_add_num.json', 'w') as file:
            json.dump(self.had_perception_info_dict["total_model_label_classify_need_add_num"], file)

    def print_every_model_classify_need_add_test_num(self):
        for model_name in self.had_perception_info_dict["total_model_label_classify_need_add_num"]:
            # 假设有以下字典
            my_dict = self.had_perception_info_dict["total_model_label_classify_need_add_num"][model_name]
            # 使用sorted函数和lambda表达式来根据值进行从大到小的排序
            sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse=True))
            print(model_name,sorted_dict)

had_perception_sample_info = HadPerceptionTestSampleInfo()
had_perception_sample_info.read_test_sample_classify_info()
had_perception_sample_info.get_test_sample_classify_number()
had_perception_sample_info.calculate_label_classify_need_add_num()
had_perception_sample_info.print_every_model_classify_need_add_test_num()