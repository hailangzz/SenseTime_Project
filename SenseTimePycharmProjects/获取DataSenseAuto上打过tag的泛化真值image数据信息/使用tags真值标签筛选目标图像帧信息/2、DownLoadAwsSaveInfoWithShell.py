# 使用/data/data_senseauto/bucket_tag_data/download_tags_file_shell 目录下的AWS文件下载指令下载tags真值数据中的如下文件：
# 使用ads-cli 命令进行tags相关文件下载
#   data-tag.json、center_camera_fov30.txt、center_camera_fov120.txt、rear_camera.txt
import os
import subprocess

class DownLoadAwsSaveInfoWithShell:
    def __init__(self,aws_download_shell,down_load_file_name_list,save_had_tags_info_path):
        self.image_save_bucket_info = {
                                       "tags_collection_type": "Data_Collection",
                                       "month": "2024_09",
                                       "daytime": "2024_09_08",
                                       "minute": "2024_09_08_11_10_10_hadGtParser",
                                       }

        self.aws_download_shell = aws_download_shell
        self.down_load_file_name_list = down_load_file_name_list
        self.save_had_tags_info_path =save_had_tags_info_path
        self.read_aws_download_shell()


        pass
    def read_aws_download_shell(self):
        cur = open(self.aws_download_shell,"r")
        all_download_info = cur.readlines()
        for row_info in all_download_info:
            for file_name in self.down_load_file_name_list:

                row_info_split_list = row_info.split(" ")
                image_save_bucket_path_info = row_info_split_list[4]
                split_bucket_info_split = \
                image_save_bucket_path_info.split("/HAD/Data_Collection/GT_data/hadGtParser/")[-1].split("/")
                self.image_save_bucket_info["tags_collection_type"] = split_bucket_info_split[0]
                self.image_save_bucket_info["month"] = split_bucket_info_split[1]
                self.image_save_bucket_info["daytime"] = split_bucket_info_split[2]
                self.image_save_bucket_info["minute"] = split_bucket_info_split[3]
                add_daytime_save_path = os.path.join(self.save_had_tags_info_path,
                                                     self.image_save_bucket_info["tags_collection_type"],
                                                     self.image_save_bucket_info["month"],
                                                     self.image_save_bucket_info["daytime"],
                                                     self.image_save_bucket_info["minute"])
                row_info_split_list[5] = add_daytime_save_path
                self.down_load_command_list = []
                self.down_load_command_list = row_info_split_list[:4]
                bucket_source_path = ""
                bucket_save_path=""
                if "camera" in file_name:
                    row_info_split_list[4] = row_info_split_list[4][:-1] + "/camera/" + file_name + '"'
                    row_info_split_list[5] = '"'+row_info_split_list[5].strip()[:-1] + "/" + file_name + '"'
            #
                else:
                    row_info_split_list[4] = row_info_split_list[4][:-1] + "/" + file_name + '"'
                    row_info_split_list[5] = '"' + row_info_split_list[5].strip()[:-1] + "/" + file_name + '"'



                print(row_info_split_list)
                dowmload_command = " ".join(row_info_split_list)
                print(dowmload_command)
                result = subprocess.run([dowmload_command], shell=True, capture_output=True, text=True)
            # # print(row_info_split_list)

                #
                # # 对文件tags文件存储路径进行修正，增加daytime目录结构

                #
                # print(add_daytime_save_path)
                # add_daytime_save_path = add_daytime_save_path.split('/')
                # add_daytime_save_path.insert(5,add_daytime_save_path[5][:10])  # 增加daytime目录结构信息
                # print(add_daytime_save_path)
                # row_info_split_list[5] = "/".join(add_daytime_save_path)
                # print(row_info_split_list[5])
                #
                # if "camera" in file_name:
                #     row_info_split_list[4] = row_info_split_list[4][:-1] + "/camera/" + file_name + '"'
                #     row_info_split_list[5] = row_info_split_list[5].strip()[:-1] + "/" + file_name + '"'
                #     result_row_info = " ".join(row_info_split_list)
                #     result = subprocess.run([result_row_info], shell=True, capture_output=True, text=True)
                # else:
                #     row_info_split_list[4] = row_info_split_list[4][:-1] + "/" + file_name + '"'
                #     row_info_split_list[5] = row_info_split_list[5].strip()[:-1] + "/" + file_name + '"'
                #     result_row_info = " ".join(row_info_split_list)
                #     result = subprocess.run([result_row_info], shell=True, capture_output=True, text=True)
                # print(result_row_info)
                #



      




aws_download_shell = "/data/data_senseauto/bucket_tag_data/download_tags_file_shell/roadmarker_HAD_tags/roadmarker_202409_HAD_tags_L_U_turn_1.sh"
save_had_tags_info_path = r"/data/data_senseauto/bucket_tag_data/HAD_tags_info_folder/roadmarker/202409"
#'center_camera_fov30.txt','center_camera_fov120.txt','rear_camera.txt'
down_load_file_name_list = ["data-tag.json",'center_camera_fov30.txt','center_camera_fov120.txt','rear_camera.txt']
down_load_aws_info = DownLoadAwsSaveInfoWithShell(aws_download_shell,down_load_file_name_list,save_had_tags_info_path)


aaa = os.path.join("aasdf","fasdf")
print(aaa)