import os.path
import json
from collections import Counter
import copy
import subprocess


aws_config={"aws_custom_name":{}}
ak_sk_info = {"access_key":"",
              "access_key":"",
              "host_base":""
              }

total_image_bucket_file_path=[]
def download_image_with_datalist_info(total_image_bucket_file_path,aws_config):
    save_image_number = 0
    for file_path  in total_image_bucket_file_path:
        save_image_number+=1
        #save_image_path = "/data/had_test_datelist/test_image_folder/roadmarker/"+str(save_image_number)+".jpg"
        save_image_path = "/data/had_test_datelist/test_image_folder/pole/" + str(save_image_number) + ".jpg"
        # print(file_path,aws_config["aws_custom_name"][file_path.split(":")[0]])


        calling_commands = "aws --endpoint-url=" + aws_config["aws_custom_name"][file_path.split(":")[0]]["host_base"]
        profile_parameter = "--profile " + file_path.split(":")[0]
        cmd_type = "s3 cp"
        read_bucket_path = file_path.split(":",1)[-1]

        command = " ".join([calling_commands, profile_parameter, cmd_type, read_bucket_path,save_image_path])
        print(command)
        # Run the htop command
        subprocess.run([command], shell=True)
        # result = subprocess.run([command], shell=True, capture_output=True, text=True)
    # pass
    # print(aws_config["aws_custom_name"].keys())

def read_aws_petreloss_out_info(petreloss_out_path=r"/home/SENSETIME/zhangzhuo/petreloss_out.conf"):
    new_aws_custom_name = ""
    cur = open(petreloss_out_path,"r",encoding="utf-8")
    all_aws_ak_sk_info = cur.readlines()
    for row_info in all_aws_ak_sk_info:

        # row_info= row_info.strip()
        if "[" == row_info[0] and "]" in row_info:
            # print(row_info)
            new_aws_custom_name = row_info[1:-2]
            if row_info[1:-2] not in aws_config["aws_custom_name"]:
                aws_config["aws_custom_name"][new_aws_custom_name] = copy.deepcopy(ak_sk_info)

        if "access_key" in row_info[:10]:
            aws_config["aws_custom_name"][new_aws_custom_name]["access_key"] = row_info.split(" = ")[-1].strip()
        if "secret_key" in row_info[:10]:
            aws_config["aws_custom_name"][new_aws_custom_name]["secret_key"] = row_info.split(" = ")[-1].strip()
        if "host_base" in row_info[:9]:
            aws_config["aws_custom_name"][new_aws_custom_name]["host_base"] = row_info.split(" = ")[-1].strip()

    # print(aws_config["aws_custom_name"])


def sample_category(json_path, out_path=None, **sample_dict):
    label_info_lines = open(json_path, 'r', encoding='utf-8').readlines()
    total_class_label_count = Counter()
    total_class_label_image_count = Counter()


    for line in label_info_lines:
        label_single_image_set = set()
        data = json.loads(line)
        if len(data)<4:
            print(len(data))
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

        filename = data['filename']
        # print(filename)
        total_image_bucket_file_path.append(filename)


    return total_class_label_count,total_class_label_image_count



if __name__ == '__main__':
    sample_dict_ = {str(k): 100 for k in range(1, 80)}
    # sample_dict_['1'] = 20
    #json_path_ = '/data/data_after_annotation/tsr/Total_TSR_all_in_history/b21704_b21774_b21777_b21971_b22593_b24067_b24253_b25926.json'
    read_aws_petreloss_out_info()
    json_path_ = r"/data/had_test_datelist/test_pole.json"
    total_class_label_count,total_class_label_image_count = sample_category(json_path_,  **sample_dict_)
    # print(total_class_label_count)
    # print(len(total_class_label_count))
    #
    # print(total_class_label_image_count)
    # print(len(total_class_label_image_count))
    download_image_with_datalist_info(total_image_bucket_file_path,aws_config)

