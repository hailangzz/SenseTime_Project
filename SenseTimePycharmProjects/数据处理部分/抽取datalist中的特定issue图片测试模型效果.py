import os
import json
from pathlib import Path
import shutil

class SearchTargetIssueImageDatalist:
    def __init__(self,origin_datalist_path,target_datetime_list,output_search_datalist_file,origin_images_path):
        self.target_datetime_list = target_datetime_list
        self.origin_datalist_path = origin_datalist_path
        self.output_search_datalist_file = output_search_datalist_file
        self.origin_images_path =origin_images_path
        self.origin_datalist = []
        self.search_datalist = []

    def read_origin_json(self):
        with open(self.origin_datalist_path, 'r', encoding='utf-8') as f:
            all_array_info = f.readlines()
            # 使用 json.load() 方法解析JSON文件
            for array_info in all_array_info:
                result_array = json.loads(array_info)
                self.origin_datalist.append(result_array)


    def search_target_datelist(self):
        for row_of_datalist in self.origin_datalist:
            for target_datetime in self.target_datetime_list:
                if target_datetime in row_of_datalist["filename"]:
                    self.search_datalist.append(row_of_datalist)
        # print(self.search_datalist)

    def save_to_json(self):

        with open(self.output_search_datalist_file, 'w') as json_file:
            for row_dict_info in self.search_datalist:
                json_file.write(json.dumps(row_dict_info))
                json_file.write("\n")
        json_file.close()

    def save_search_datalist_images(self):

        fater_path = Path(self.origin_images_path)
        parent_path = fater_path.parent  # 获取上一层路径
        save_search_image_director_name = self.output_search_datalist_file.split('/')[-1].replace(".json","")
        save_search_image_director_path = os.path.join(parent_path,save_search_image_director_name) # 存储筛选图片的路径
        if not os.path.exists(save_search_image_director_path):
            os.mkdir(save_search_image_director_path)

        for search_datetime in self.target_datetime_list:
            source_dir = os.path.join(self.origin_images_path,search_datetime)
            destination_dir = os.path.join(save_search_image_director_path,search_datetime)

            # 拷贝目标图片
            # 使用shutil的copytree函数拷贝文件夹
            try:
                shutil.copytree(source_dir, destination_dir)
                print(f"文件夹 {source_dir} 已被拷贝到 {destination_dir}")
            except OSError as e:
                # 如果目标文件夹已存在，shutil.copytree会抛出异常
                # 这里可以选择覆盖目标文件夹（需要先删除它），或者给出提示
                if e.errno == 17:
                    # errno 17 表示目标文件夹已存在
                    print(f"目标文件夹 {destination_dir} 已存在，请先删除或选择另一个位置。")
                else:
                    # 处理其他类型的OSError
                    print(f"拷贝过程中发生错误: {e}")
            except Exception as e:
                # 处理其他可能的异常
                print(f"拷贝过程中发生未知错误: {e}")



#output_search_datalist_file = r"./TLR_L4_list_part_mixed_mode_light.json"
output_search_datalist_file = r"./TLR_L4_list_part_2024_06_12_15_21_41.json"
origin_datalist_path = r"./TLR_L4_list.json"
target_datetime_list = ["2024_06_12_15_21_41"]
origin_images_path = "/data/TLR/L4_snap"

search_target_image_datalist = SearchTargetIssueImageDatalist(origin_datalist_path,target_datetime_list,output_search_datalist_file,origin_images_path)
search_target_image_datalist.read_origin_json()
search_target_image_datalist.search_target_datelist()
search_target_image_datalist.save_to_json()
search_target_image_datalist.save_search_datalist_images()