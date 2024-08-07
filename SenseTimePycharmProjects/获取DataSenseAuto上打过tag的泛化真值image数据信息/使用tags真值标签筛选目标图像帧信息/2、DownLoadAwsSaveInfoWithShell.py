# 使用/data/data_senseauto/bucket_tag_data/download_tags_file_shell 目录下的AWS文件下载指令下载tags真值数据中的如下文件：
# 使用ads-cli 命令进行tags相关文件下载
#   data-tag.json、center_camera_fov30.txt、center_camera_fov120.txt、rear_camera.txt
import os
import path
import subprocess

class DownLoadAwsSaveInfoWithShell:
    def __init__(self,aws_download_shell,down_load_file_name_list):
        self.aws_download_shell = aws_download_shell
        self.down_load_file_name_list = down_load_file_name_list
        self.read_aws_download_shell()
        pass
    def read_aws_download_shell(self):
        cur = open(self.aws_download_shell,"r")
        all_download_info = cur.readlines()
        for row_info in all_download_info:
            for file_name in self.down_load_file_name_list:
                row_info_split_list = row_info.split(" ")
                # 对文件tags文件存储路径进行修正，增加daytime目录结构
                add_daytime_save_path = row_info_split_list[5]
                add_daytime_save_path = add_daytime_save_path.split('/')
                add_daytime_save_path.insert(5,add_daytime_save_path[5][:10])  # 增加daytime目录结构信息
                # print(add_daytime_save_path)
                row_info_split_list[5] = "/".join(add_daytime_save_path)

                if "camera" in file_name:
                    row_info_split_list[4] = row_info_split_list[4][:-1] + "/camera/" + file_name + '"'
                    row_info_split_list[5] = row_info_split_list[5].strip()[:-1] + "/" + file_name + '"'
                    result_row_info = " ".join(row_info_split_list)
                    result = subprocess.run([result_row_info], shell=True, capture_output=True, text=True)
                else:
                    row_info_split_list[4] = row_info_split_list[4][:-1] + "/" + file_name + '"'
                    row_info_split_list[5] = row_info_split_list[5].strip()[:-1] + "/" + file_name + '"'
                    result_row_info = " ".join(row_info_split_list)
                    result = subprocess.run([result_row_info], shell=True, capture_output=True, text=True)
                print(result_row_info)




      




aws_download_shell = "/data/data_senseauto/bucket_tag_data/download_tags_file_shell/TurnAround_1_TLR_0806.sh"
#'center_camera_fov30.txt','center_camera_fov120.txt','rear_camera.txt'
down_load_file_name_list = ["data-tag.json",'center_camera_fov30.txt','center_camera_fov120.txt','rear_camera.txt']
down_load_aws_info = DownLoadAwsSaveInfoWithShell(aws_download_shell,down_load_file_name_list)


aaa = os.path.join("aasdf","fasdf")
print(aaa)