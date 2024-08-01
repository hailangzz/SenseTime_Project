import os

def count_files_recursive(path):
    # 初始化计数器
    count = 0

    # 遍历路径下的所有文件和文件夹
    for item in os.listdir(path):
        # 拼接完整的路径
        item_path = os.path.join(path, item)

        # 如果是文件，计数器加一
        if os.path.isfile(item_path):
            count += 1
        # 如果是文件夹，递归调用count_files_recursive，并累加结果
        elif os.path.isdir(item_path):
            count += count_files_recursive(item_path)

    return count

# 测试
path = '/data/data_after_annotation/tsr/236_tsr_16254/b22418_test_snap'  # 替换成你想统计的路径
# # path = "/data/Generalization/G5/animal/autolabel_sdcoss3:s3:/sdc3_faw/HAD/Data_Collection/GT_data/hadGtParser/HAD_gt_2dRoadSemantic/2024_06/2024_06_09"
# # path = "/data/Generalization/G5/animal/autolabel_sdcoss3:s3:/sdc3_faw/HAD/Data_Collection/GT_data/hadGtParser/HAD_gt_2dRoadSemantic/2024_06/2024_06_09/2024_06_09_15_41_07_parser"
# path = "/data/Generalization/G5/animal/autolabel_sdcoss3:s3:/sdc3_faw/HAD/Data_Collection/GT_data/hadGtParser/HAD_gt_2dRoadSemantic/2024_06/2024_06_09/2024_06_09_15_42_07_parser"

file_count = count_files_recursive(path)
print(f"Total files in {path} and its subdirectories: {file_count}")

