import os
import subprocess
from datetime import datetime, timedelta

class GetImageAwsSaveInfo:

    def __init__(self,search_datetime_range={"start_date":"2024_09_03","end_date":"2024_09_12"}):
        # self.aws_server_URL = "http://sdc-oss-3.iagproxy.senseauto.com"
        # self.aws_credentials = "ad_system_common"
        # self.aws_bucket_name = "s3://sdc3_faw"

        self.aws_server_URL = "http://auto-oss.iagproxy.senseauto.com"
        self.aws_credentials = "ad_system_common"
        self.aws_bucket_name = "s3://sdc3-faw-2"

        self.aws_bucket_total_info_dict={}
        self.program_version_ = "V_0.1"

        self.save_bucket_tag_data_path = r"/data/data_senseauto/bucket_tag_data/AWS_DATA_daytime"
        self.search_datetime_range = search_datetime_range
        self.search_datetime_monthdate_daytime_info={"monthdate":[],
                                                     "daytime":[]}
        self.init_search_datetime_monthdate_and_daytime_info()

    def print_program_version(self):
        print(self.program_version_)

    def init_search_datetime_monthdate_and_daytime_info(self):
        interval_day = 1 # 天数间隔
        # 定义日期时间字符串的格式
        date_format = "%Y_%m_%d"
        # 使用 strptime 将字符串转换为 datetime 对象
        start_date_obj = datetime.strptime(self.search_datetime_range["start_date"], date_format)
        end_date_obj = datetime.strptime(self.search_datetime_range["end_date"], date_format)

        # 生成在开始和截止日期时间之间的连续日期时间
        current_datetime = start_date_obj

        while current_datetime <= end_date_obj:
            string_datetime = current_datetime.strftime(date_format)
            self.search_datetime_monthdate_daytime_info["daytime"].append(string_datetime)
            monthdate_string = string_datetime[:7]
            if monthdate_string not in self.search_datetime_monthdate_daytime_info["monthdate"]:
                self.search_datetime_monthdate_daytime_info["monthdate"].append(monthdate_string)
            current_datetime += timedelta(days=interval_day)

    def read_aws_data_bucket_path_directory_list(self,data_bucket_path = "/HAD/Data_Collection/GT_data/hadGtParser/HAD_gt_PVB/",cmd_type="s3 ls"):

        bucket_subdirectory_monthdate = []
        bucket_subdirectory_daytimedate = []
        try:
            calling_commands = "aws --endpoint-url="+self.aws_server_URL
            profile_parameter = "--profile "+self.aws_credentials
            cmd_type = "s3 ls"
            read_bucket_path = self.aws_bucket_name+data_bucket_path

            command = " ".join([calling_commands,profile_parameter,cmd_type,read_bucket_path])
            # Run the htop command
            #subprocess.run([command], shell=True)
            result = subprocess.run([command],shell=True, capture_output=True, text=True)
            # print(result.stdout,type(result.stdout))
            for monthdate_name in result.stdout.split('/'):
                monthdate = monthdate_name.strip().replace("PRE ",'')
                # print(monthdate)

                # if len(monthdate)!=0 and monthdate!="2024_05":         #筛选需要的月份
                if len(monthdate) != 0 and monthdate in self.search_datetime_monthdate_daytime_info["monthdate"]:  # 筛选需要的月份
                    bucket_subdirectory_monthdate.append(monthdate)
                    if monthdate not in self.aws_bucket_total_info_dict:
                        self.aws_bucket_total_info_dict[monthdate]={} #将aws桶数据目录的，月份目录信息记录的数据桶字典表中

                    read_bucket_daytime_directory_command = command+monthdate+'/'
                    #print(read_bucket_daytime_directory_command)
                    result = subprocess.run([read_bucket_daytime_directory_command], shell=True, capture_output=True, text=True)

                    for daytime_name in result.stdout.split('/'):
                        daytime = daytime_name.strip().replace("PRE ", '')
                        # print(daytime)
                        if len(daytime) != 0 and daytime in self.search_datetime_monthdate_daytime_info["daytime"]:                            #筛选需要的日
                            if daytime not in self.aws_bucket_total_info_dict[monthdate]:
                                self.aws_bucket_total_info_dict[monthdate][daytime] = {}  # 将aws桶数据目录的，日目录信息记录的数据桶字典表中
                            bucket_subdirectory_daytimedate.append(daytime)
                            read_bucket_minute_directory_command = read_bucket_daytime_directory_command + daytime + '/'
                            result = subprocess.run([read_bucket_minute_directory_command], shell=True,
                                                    capture_output=True, text=True)

                            for minute_name in result.stdout.split('/'):
                                minute_name = minute_name.strip().replace("PRE ", '')
                                if len(minute_name) != 0:
                                    if minute_name not in self.aws_bucket_total_info_dict[monthdate][daytime]:
                                        cp_bucket_minute_directory_command =read_bucket_minute_directory_command.replace("s3 ls ","s3 cp ")
                                        self.aws_bucket_total_info_dict[monthdate][daytime][minute_name] = {"data-tag.json":cp_bucket_minute_directory_command+minute_name+"/data-tag.json",
                                                                                                            "center_camera_fov120.txt": cp_bucket_minute_directory_command + minute_name + "/camera/center_camera_fov120.txt",
                                                                                                            "center_camera_fov30.txt": cp_bucket_minute_directory_command + minute_name + "/camera/center_camera_fov30.txt",
                                                                                                            "rear_camera.txt": cp_bucket_minute_directory_command + minute_name + "/camera/rear_camera.txt",
                                                                                                            }  # 将aws桶数据目录的，分钟切片目录信息记录的数据桶字典表中
                                        # print(self.aws_bucket_total_info_dict[monthdate][daytime][minute_name])
            # print(index,bucket_subdirectory_monthdate)

        except FileNotFoundError:
            print("read aws bucket path directory list info error.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def cp_data_senseauto_bucket_tag_data(self):
        save_monthdate_directory_path = ""
        save_daytime_directory_path = ""
        save_minute_directory_path = ""

        for monthdate in self.aws_bucket_total_info_dict:
            save_monthdate_directory_path = os.path.join(self.save_bucket_tag_data_path,monthdate)
            if not os.path.exists(save_monthdate_directory_path):
                os.mkdir(save_monthdate_directory_path)
            for daytime in self.aws_bucket_total_info_dict[monthdate]:
                save_daytime_directory_path = os.path.join(self.save_bucket_tag_data_path,monthdate,daytime)
                if not os.path.exists(save_daytime_directory_path):
                    os.mkdir(save_daytime_directory_path)
                for minute in self.aws_bucket_total_info_dict[monthdate][daytime]:
                    save_minute_directory_path = os.path.join(self.save_bucket_tag_data_path, monthdate, daytime,minute)
                    if not os.path.exists(save_minute_directory_path):
                        os.mkdir(save_minute_directory_path)
                    for minute_bucket_tag_file_name in self.aws_bucket_total_info_dict[monthdate][daytime][minute]:
                        print(minute_bucket_tag_file_name)
                        print(self.aws_bucket_total_info_dict[monthdate][daytime][minute][minute_bucket_tag_file_name])
                        cp_minute_bucket_tag_file_command = self.aws_bucket_total_info_dict[monthdate][daytime][minute][minute_bucket_tag_file_name] + " " + save_minute_directory_path + "/"+minute_bucket_tag_file_name
                        subprocess.run([cp_minute_bucket_tag_file_command], shell=True)


if __name__ == "__main__":
    search_datetime_range = {"start_date":"2024_09_03","end_date":"2024_09_12"}
    task = GetImageAwsSaveInfo(search_datetime_range)
    task.print_program_version()
    task.read_aws_data_bucket_path_directory_list()
    task.cp_data_senseauto_bucket_tag_data()