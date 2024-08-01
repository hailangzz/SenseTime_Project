import pandas as pd
import openpyxl
import json
import os
def get_Retrieve_annotation_file_information(file_path):

    resulte_info_dict = {"annotation_errors_total_number":0,
                         "annotation_errors_images_number": 0,
                         "P0_errors_number":0,
                         "P1_errors_number": 0
                         }
    # 读取Excel文件
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    data = pd.DataFrame(sheet.values)

    resulte_info_dict["annotation_errors_total_number"] = len(data)
    resulte_info_dict["annotation_errors_images_number"] = len(set(data[0]))
    resulte_info_dict["P0_errors_number"] = len(data[data[2]=="标注错误"])
    resulte_info_dict["P1_errors_number"] = len(data[data[2] == "标注模糊"])
    # print(len(data))
    # print(data[0],type(data[0]),data[0].values,len(set(data[0])))
    # print(len(data[data[2]=="标注错误"]))
    # print(len(data[data[2] == "标注模糊"]))
    return resulte_info_dict

def get_test_json_info(test_json_file):

    # total_annotation_numbers = 0
    # with open(test_json_file, 'r', encoding='utf-8') as f:
    #     all_array_info = f.readlines()
    #     # 使用 json.load() 方法解析JSON文件
    #     for array_info in all_array_info:
    #         result_array = json.loads(array_info)
    #
    #         total_annotation_numbers += len(result_array['instances'])
    #         # print(len(result_array['instances']))
    # return total_annotation_numbers

    total_annotation_numbers = 0
    # 遍历路径下的所有文件和文件夹
    for item in os.listdir(test_json_file):
        # 拼接完整的路径
        item_path = os.path.join(test_json_file, item)

        # 如果是文件，计数器加一
        if os.path.isfile(item_path):
            total_annotation_numbers += 1
        # 如果是文件夹，递归调用count_files_recursive，并累加结果
        elif os.path.isdir(item_path):
            total_annotation_numbers += get_test_json_info(item_path)
    return total_annotation_numbers


test_sampling_quantity = 1886
file_path = r"/data/data_after_annotation/tsr/236_tsr_16254/b22418_test_snap/b22418_test_comment.xlsx"
# test_json_file = r"/data/data_after_annotation/tsr/236_tsr_16254/b22418_test.json"
test_json_file = "/data/data_after_annotation/tsr/236_tsr_16254/b22418_test_snap"
resulte_info_dict = get_Retrieve_annotation_file_information(file_path)
total_annotation_numbers = get_test_json_info(test_json_file)

print(resulte_info_dict)
print("标注质量信息统计：",)
print("抽检数量：{test_sampling_quantity}".format(test_sampling_quantity =test_sampling_quantity))
print("标注框总数量：{total_annotation_numbers}".format(total_annotation_numbers =total_annotation_numbers))
print("P0:：{P0_errors_number}".format(P0_errors_number =resulte_info_dict["P0_errors_number"]))
print("P1：{P1_errors_number}".format(P1_errors_number =resulte_info_dict["P1_errors_number"]))

print("图片级错误率：{images_error_rate}, 潜在标签类别错误：{annotation_errors_total_number}".format(images_error_rate=resulte_info_dict["annotation_errors_images_number"]/test_sampling_quantity,
                                                            annotation_errors_total_number=resulte_info_dict["annotation_errors_total_number"]))
print("标签错误率：{target_errors_rate}".format(target_errors_rate = resulte_info_dict["annotation_errors_total_number"]/total_annotation_numbers))
