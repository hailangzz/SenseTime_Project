import os
import json
import copy
from tqdm import tqdm



class CommonClassify:
    def __init__(self):
        self.GT_filename_dict = {}
        self.useful_predict_result_list= []
        pass

    def read_ground_true_datalist(self,GT_path):
        gt_info_lines = open(GT_path, 'r', encoding='utf-8').readlines()
        # for line in gt_info_lines:
        for line_index in tqdm(range(len(gt_info_lines))):
            line = gt_info_lines[line_index]
            data = json.loads(line)
            # print(data['filename'])

            self.GT_filename_dict[data['filename']]=1

        pass


    def read_predict_result_datalist(self,predict_result_path):
        # predict_result_info_lines = open(predict_result_path, 'r', encoding='utf-8').readlines()
        # print(predict_result_info_lines[1])
        unuseful_image_bucket_cur = open(r"/data/unuseful_bucket_image_path.txt",'w')
        predcit_info_lines = open(predict_result_path, 'r', encoding='utf-8').readlines()
        for line in predcit_info_lines:
            cover_data = eval(line)
            # print(line[-200:])
            # data = json.loads(line)
            # for single_predict_result in data:
            for line_index in tqdm(range(len(cover_data))):
                single_predict_result = cover_data[line_index]

                predict_result_image_bucket_path = single_predict_result['image_id']
                try:
                    if self.GT_filename_dict[predict_result_image_bucket_path]:
                    # if predict_result_image_bucket_path in self.GT_filename_dict:
                        self.useful_predict_result_list.append(copy.deepcopy(single_predict_result))
                        # self.useful_predict_result_list.append(single_predict_result)
                    else:
                        pass
                except:
                    unuseful_image_bucket_cur.write(predict_result_image_bucket_path)
                    unuseful_image_bucket_cur.write("\n")

                    continue
        unuseful_image_bucket_cur.close()

    def save_resule_data(self,predict_result_path):
        save_path = os.path.join(predict_result_path.split("results.txt")[0],"save_results.txt")
        with open(save_path, 'w') as f:
            json.dump(self.useful_predict_result_list, f)
        pass
