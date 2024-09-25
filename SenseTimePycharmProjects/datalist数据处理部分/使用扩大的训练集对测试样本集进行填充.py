import os
import json
import random

class HadPeceptionTestDatalistExpand:

    def __init__(self):
        self.pereception_model_name_list = ["tlr", "tsr", "obstacle", "roadmarker", "pole", "rm_roadmarker", "rm_pole", "animal"]
        #self.pereception_model_name_list = ["tlr"]
        self.label_classify_need_add_num_json = "label_classify_need_add_num.json"
        self.had_perception_info_dict = {

            "total_model_train_datalist_path": {
                "tlr": "/data/FAW_HAD/datalists/tlr/train.json",
                "tsr": "/data/FAW_HAD/datalists/tsr/train.json",
                "obstacle": "/data/FAW_HAD/datalists/obstacle/train.json",
                "roadmarker": "/data/FAW_HAD/datalists/roadmarker/train.json",
                "pole": "/data/FAW_HAD/datalists/pole/train.json",
                "rm_roadmarker": "/data/FAW_HAD/datalists/rearRM/train.json",
                "rm_pole": "/data/FAW_HAD/datalists/pole/train.json",
                "animal": "/data/FAW_HAD/datalists/animal/train.json"},

            "total_model_train_datalist_classify_images_info":{
                "tlr": {},
                "tsr": {},
                "obstacle": {},
                "roadmarker": {},
                "pole": {},
                "rm_roadmarker": {},
                "rm_pole": {},
                "animal": {},
            },
            "total_model_train_datalist_classify_images_number": {
                "tlr": {},
                "tsr": {},
                "obstacle": {},
                "roadmarker": {},
                "pole": {},
                "rm_roadmarker": {},
                "rm_pole": {},
                "animal": {},
            },
        }
        self.output_file = "/data/data_after_annotation/expend_model_test_datalist"
        self.read_relevant_information()
        self.print_order_train_datalist_classify_num()
    def read_datalist_json_info(self,model_name):
        row_id = 0
        datalist_json_path = self.had_perception_info_dict["total_model_train_datalist_path"][model_name]
        with open(datalist_json_path, 'r',
                  encoding='utf-8') as f:
            all_array_info = f.readlines()
            # 使用 json.load() 方法解析JSON文件
            for array_info in all_array_info:  # 每一个图片样本的标注记录
                row_id+=1
                if row_id%1000==0:
                    print(row_id)
                result_array = json.loads(array_info)

                for singel_label_info in result_array["instances"]:  # 每张图片标注信息的单个标注框信息
                    if singel_label_info["label"] not in \
                            self.had_perception_info_dict["total_model_train_datalist_classify_images_info"][model_name]:
                        self.had_perception_info_dict["total_model_train_datalist_classify_images_info"][model_name][
                            singel_label_info["label"]] = []

                    if result_array["filename"] not in \
                            self.had_perception_info_dict["total_model_train_datalist_classify_images_info"][model_name][
                                singel_label_info["label"]]:
                        self.had_perception_info_dict["total_model_train_datalist_classify_images_info"][model_name][
                            singel_label_info["label"]].append(result_array)

        #记录训练集每个模型对应的标签类别图片数量：
        for classify_name in self.had_perception_info_dict["total_model_train_datalist_classify_images_info"][model_name]:
            self.had_perception_info_dict["total_model_train_datalist_classify_images_number"][model_name][classify_name]=len(self.had_perception_info_dict["total_model_train_datalist_classify_images_info"][model_name][classify_name])
    def print_order_train_datalist_classify_num(self):
        for model_name in self.pereception_model_name_list:
            # print(model_name)
            my_dict = self.had_perception_info_dict["total_model_train_datalist_classify_images_number"][model_name]
            # 使用sorted函数和lambda表达式来根据值进行从大到小的排序
            sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse=True))
            print(model_name, sorted_dict)

    def save_to_json(self, model_name,random_expand_train_datalist_list):

        output_file = os.path.join(self.output_file,model_name+"_test_expand.json")
        with open(output_file, 'w',encoding='utf-8') as json_file:
            for row_dict_info in random_expand_train_datalist_list:
                # print(row_dict_info)
                json_file.write(json.dumps(row_dict_info,ensure_ascii=False))
                json_file.write("\n")
        json_file.close()

    def read_relevant_information(self):

        # 读取不同模型每个分类的测试文件，缺少样本的个数
        with open('label_classify_need_add_num.json', 'r') as file:
            label_classify_need_add_num_data = json.load(file)
            # print(label_classify_need_add_num_data)
        for model_name in self.pereception_model_name_list:
            print(model_name,label_classify_need_add_num_data[model_name])
            self.read_datalist_json_info(model_name)
            for classify_name in label_classify_need_add_num_data[model_name]:
                if label_classify_need_add_num_data[model_name][classify_name]!=0:
                    list_of_total_train_image_path = self.had_perception_info_dict["total_model_train_datalist_classify_images_info"][model_name][int(classify_name)]
                    # 如果训练集中有足够数量的样本时
                    if self.had_perception_info_dict["total_model_train_datalist_classify_images_number"][model_name][int(classify_name)]>=label_classify_need_add_num_data[model_name][classify_name]:
                        random_expand_train_datalist_list = random.sample(list_of_total_train_image_path, label_classify_need_add_num_data[model_name][classify_name])
                    # 如果训练集中样本不足时
                    else:
                        random_expand_train_datalist_list = random.sample(list_of_total_train_image_path,
                                                                          self.had_perception_info_dict["total_model_train_datalist_classify_images_number"][model_name][classify_name])
                    # print(random_expand_train_datalist_list)
            self.save_to_json(model_name,random_expand_train_datalist_list)



had_peception_object = HadPeceptionTestDatalistExpand()