import os
import json
import copy

class CheckInferResultsInfo:
    def __init__(self, pretraining_infer_results_save_path):
        self.pretraining_infer_results_save_path = premodel_infer_results_save_path
        self.check_infer_score_threshold = 0.4
        self.check_infer_results_list = []

    def read_infer_results_file(self):
        with open(self.pretraining_infer_results_save_path, 'r', encoding='utf-8') as f:
            all_array_info = f.readlines()
            # 使用 json.load() 方法解析JSON文件
            for array_info in all_array_info:
                result_array = json.loads(array_info)
                for single_infer_result in result_array:
                    if single_infer_result["score"]>= self.check_infer_score_threshold:
                        self.check_infer_results_list.append(copy.deepcopy(single_infer_result))


    def save_check_results(self):
        print(len(self.check_infer_results_list))
        # 将字典保存为JSON文件
        with open('check_results.txt', 'w', encoding='utf-8') as f:
            json.dump(self.check_infer_results_list, f)


premodel_infer_results_save_path = "/data/Generalization/G5/animal/results.txt"
check_infer_results = CheckInferResultsInfo(premodel_infer_results_save_path)
check_infer_results.read_infer_results_file()
check_infer_results.save_check_results()






