import os.path
import random
import json
from collections import Counter

def sample_category(json_path, out_path=None, **sample_dict):
    label_info_lines = open(json_path, 'r', encoding='utf-8').readlines()
    total_class_label_count = Counter()
    total_class_label_image_count = Counter()

    random.shuffle(label_info_lines)
    for line in label_info_lines:
        label_single_image_set = set()
        data = json.loads(line)
        instances = data['instances']
        if not instances:
            continue
        for ins in instances:
            if 'label' not in ins or ins['is_ignored']:
                continue
            label = str(ins['label'])
            total_class_label_count[label]+=1   # 统计所有的标注类别，样本框个数；

            if label not in label_single_image_set:  # 每张图片中单个类别label,如果已经有一个，则算一张样本
                total_class_label_image_count[label] += 1
            label_single_image_set.add(label)

    return total_class_label_count,total_class_label_image_count



if __name__ == '__main__':
    sample_dict_ = {str(k): 100 for k in range(1, 80)}
    # sample_dict_['1'] = 20
    json_path_ = '/data/data_after_annotation/tsr/Total_TSR_all_in_history/b21704_b21774_b21777_b21971_b22593_b24067_b24253_b25926.json'
    total_class_label_count,total_class_label_image_count = sample_category(json_path_,  **sample_dict_)
    print(total_class_label_count)
    print(len(total_class_label_count))

    print(total_class_label_image_count)
    print(len(total_class_label_image_count))
