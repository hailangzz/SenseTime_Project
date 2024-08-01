#!/usr/bin/env python
# encoding:utf-8
"""
author: liusili
@contact: liusili@sensetime.com
@software:
@file: select_data.py
@time: 2021/8/13
@desc:
"""
import sys
import os
import json

import fontTools.cffLib
from tqdm import tqdm


class DataSelection(object):
    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def read_json(file_path):
        lines = open(file_path, 'r', encoding='utf-8').readlines()
        return lines

    def select_data(self, label_lst, save_path=None):
        print('[START] Select data ...')
        if not save_path:
            save_path = os.path.splitext(self.file_path)[0] + '_select.json'
        f = open(save_path, 'w', encoding='utf-8')
        pbar = tqdm(self.read_json(self.file_path), file=sys.stdout)
        for line in pbar:
            data = json.loads(line)
            keep_flag = False
            for instance in data['instances']:
                if 'label' in instance and instance['label'] in label_lst:
                    keep_flag = True
            if keep_flag:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
        f.close()
        print(f'[FINISH] Data Selection has been saved @{save_path} ')

    def pick_label(self, label_lst, save_path=None):
        print('[START] Select data ...')
        if not save_path:
            save_path = os.path.splitext(self.file_path)[0] + '_pick.json'
        f = open(save_path, 'w', encoding='utf-8')
        pbar = tqdm(self.read_json(self.file_path), file=sys.stdout)
        for line in pbar:
            data = json.loads(line)
            new_instances = []
            for instance in data['instances']:
                if 'label' in instance and instance['label'] in label_lst:
                    new_instances.append(instance)
            if new_instances:
                data['instances'] = new_instances
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
        f.close()
        print(f'[FINISH] Data Selection has been saved @{save_path} ')


if __name__ == '__main__':
    file_path_ = '/data/data_after_annotation/tsr/tsr_522_1_5w/b22117.json'
    ds = DataSelection(file_path_)
    label_lst_ = list(range(1,41)) + [43,44,45,79]
    ds.select_data(label_lst_)

