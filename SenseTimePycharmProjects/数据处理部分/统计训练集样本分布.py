#!/usr/bin/env python
# encoding:utf-8
"""
author: liusili
@contact: liusili@sensetime.com
@software:
@file: sample_data.py
@time: 2021/6/2
@desc:
"""

"""
animal_cls4.yml  lightspot_cls14.yml  lightspot_cls7.yml  pole.yml              tlr_att3.yml   tlr_cls22.yml  tsr_cls83.yml
board.yml        lightspot_cls3.yml   obstacle_cls6.yml   roadmarker_cls44.yml  tlr_cls21.yml  tsr_cls79.yml  tsr_cls_faw.yml
"""

import os.path
import random
import json
from collections import Counter


def sample_category(json_path, out_path=None, **sample_dict):
    lines = open(json_path, 'r', encoding='utf-8').readlines()
    total = Counter()
    cnt = Counter()
    if not out_path:
        out_path = os.path.splitext(json_path)[0] + '_exp.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        random.shuffle(lines)
        for line in lines:
            data = json.loads(line)
            instances = data['instances']
            label_set = set()
            if not instances:
                continue
            for ins in instances:
                if 'label' not in ins or ins['is_ignored']:
                    continue
                label = str(ins['label'])
                if label not in label_set:  #每张图片中单个类别label,如果已经有一个，则算一张样本
                    total[label] += 1       #统计选取的样本的总共标签框个数
                label_set.add(label)

            # 如果只有一类，并且该类已经超过给定数量则跳过
            if len(label_set) == 1 and label in sample_dict and cnt[label] >= sample_dict[label]:
                continue

            # 如果label不在sample_dict中则一定会保留
            for lab in label_set:
                if lab not in sample_dict or cnt[lab] <= sample_dict[lab]:
                    f.write(line)
                    for label in label_set:
                        cnt[label] += 1
                    break
            # if len(set(sample_dict)) >= len(label_set | set(sample_dict)) and \
            #         label in sample_dict and sample_dict[label] <= cnt[label]:
            #     continue
            # f.write(line)
    f.close()
    print(total)
    print(cnt)
    print('finish')
    print(len(cnt))


if __name__ == '__main__':
    sample_dict_ = {str(k): 100 for k in range(1, 80)}
    # sample_dict_['1'] = 20
    json_path_ = '/data/data_after_annotation/tlr/Total_TLR_all_in_history/b25866_b24233_b24066_b22592_b21771_b21716_b21710_b21346_b21013.json'
    sample_category(json_path_,  **sample_dict_)

