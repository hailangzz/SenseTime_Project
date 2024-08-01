import os
import datetime
import shutil

class UseTagInfoGetTargetImage:
    def __init__(self, tag_file_path, image_frame_path,save_target_image_path,snap_image_save_path_txt):
        self.all_tag_info_dict = {}
        self.all_framge_image_info_dict = {}

        self.tag_file_path = tag_file_path
        self.image_frame_path = image_frame_path
        self.save_target_image_path = save_target_image_path
        self.snap_image_save_path_txt = snap_image_save_path_txt
        self.get_tag_file_info()
        self.total_copy_image_number = 0

    # 替换tag文本中，每行的图像帧信息记录上的，datetime日期字符串中的连接符，为指定连接符
    def replace_datatime_separator_symbol(self,datetime_sting,replace_char_type='-'):
        if replace_char_type=="-":
            datetime_sting = datetime_sting.replace('_','-').replace(' ', '-').replace(':', '-')
        else:
            datetime_sting = datetime_sting.replace('-', '_').replace(' ', '_').replace(':', '_')
        return datetime_sting

    # 读取解析单个tag文本文件信息
    def read_txt_info(self,txt_file_path):
        # txt_info_dict = {}
        txt_file_cur = open(txt_file_path,"r")
        all_txt_file_line = txt_file_cur.readlines()
        for single_row in all_txt_file_line:
            date_time,frame_target_string = single_row.split(',',1)
            date_time = self.replace_datatime_separator_symbol(date_time)

            if date_time not in self.all_tag_info_dict:
                self.all_tag_info_dict[date_time] = frame_target_string
            else:
                print("this datetime is repeat: ",date_time)

            # print(self.all_tag_info_dict)

    # 读取tag视频中每帧的目标信息
    def get_tag_file_info(self):
        tag_file_info_dict = {}
        tag_txt_name_list = os.listdir(self.tag_file_path)
        for tag_txt_file_name in tag_txt_name_list:
            self.read_txt_info(os.path.join(self.tag_file_path,tag_txt_file_name))
            # tag_file_info_dict[tag_txt_file_name]=[]

        # print(tag_txt_name_list)

    #将日期字符串中，日期时间调节增加8小时
    def conver_datetime_sting_to_timestamp_sting(self,datetime_string,timedelta_hours=8):
        datetime_string_delta_eight = ""
        if "-" in datetime_string:
            date_format = "%Y-%m-%d-%H-%M-%S"

            datetime_string_delta_eight = datetime_string.split('-')
            datetime_string_delta_eight[3] = str(int(datetime_string_delta_eight[3])+8)
            datetime_string_delta_eight = "-".join(datetime_string_delta_eight)
        elif "_" in datetime_string:
            date_format = "%Y_%m_%d_%H_%M_%S"
            datetime_string_delta_eight = datetime_string.split('_')
            datetime_string_delta_eight[3] = str(int(datetime_string_delta_eight[3]) + 8)
            datetime_string_delta_eight = "_".join(datetime_string_delta_eight)

        # 将字符串转换为datetime对象
        date_time_obj = datetime.datetime.strptime(datetime_string, date_format)
        time_delta = datetime.timedelta(hours=timedelta_hours)
        new_date_time_obj = date_time_obj + time_delta

        # print(str(int(new_date_time_obj.timestamp())))
        return str(int(new_date_time_obj.timestamp())),datetime_string_delta_eight

    def conver_frame_image_save_path_split_char(self,single_image_frame_director_name):
        return single_image_frame_director_name.replace("_","-")

    # 读取图像帧视频存储目录内的，所有bag视频文件夹
    def read_single_frame_image_folder(self,single_image_frame_director_path,single_image_frame_director_name):
        if single_image_frame_director_name not in self.all_framge_image_info_dict:
            #conver frame image save datetime folder split char "_" to "-"
            # #将图像帧存储父目录的分隔字符进行统一，以免后续处理时由于不统一导致遗漏
            single_image_frame_director_name = self.conver_frame_image_save_path_split_char(single_image_frame_director_name)
            self.all_framge_image_info_dict[single_image_frame_director_name]={}

            # print(single_image_frame_director_name,check_target_image_timestamp_string)
        for first_director_name in os.listdir(single_image_frame_director_path):
            if "01-CameraRadarLidar" in first_director_name:
                if first_director_name not in self.all_framge_image_info_dict[single_image_frame_director_name]:
                    self.all_framge_image_info_dict[single_image_frame_director_name][first_director_name] = {}
                # print(first_director_name)
                for second_director_name in os.listdir(os.path.join(single_image_frame_director_path,first_director_name)):

                    if os.path.isdir(os.path.join(single_image_frame_director_path,first_director_name,second_director_name)):
                        if second_director_name not in self.all_framge_image_info_dict[single_image_frame_director_name][first_director_name]:
                            self.all_framge_image_info_dict[single_image_frame_director_name][first_director_name][second_director_name]=[]
                            single_image_folder_image_name_list = os.listdir(os.path.join(single_image_frame_director_path,first_director_name,second_director_name))
                            for image_name in single_image_folder_image_name_list:
                                self.all_framge_image_info_dict[single_image_frame_director_name][first_director_name][second_director_name].append(image_name)
                                # if check_target_image_timestamp_string in image_name:
                                #     self.all_framge_image_info_dict[single_image_frame_director_name][
                                #         first_director_name][second_director_name].append(image_name)




    def get_frame_image_info(self):
        frame_image_save_folder_list = os.listdir(self.image_frame_path)
        for single_image_frame_director in frame_image_save_folder_list:
            single_image_frame_director_path = os.path.join(self.image_frame_path,single_image_frame_director)
            self.read_single_frame_image_folder(single_image_frame_director_path,single_image_frame_director)

    def check_and_change_image_save_farther_folder(self,image_path):
        if os.path.exists(image_path):
            return True
        else:
            return False
    def validate_second_range_before_and_after(self,check_target_image_timestamp_string,frame_image_name,second_num=3):
        frame_image_name_timestamp = int(frame_image_name.split('_')[4][:10])
        if abs(frame_image_name_timestamp-int(check_target_image_timestamp_string))<second_num:
            return True
        else:
            return False

    def from_tag_dict_info_check_target_image(self,chec_target_string='动物'):
        snap_image_save_path_txt_cur = open(self.snap_image_save_path_txt,'w')
        for tag_name in self.all_tag_info_dict:
            if chec_target_string in self.all_tag_info_dict[tag_name]:
                check_target_image_timestamp_string,datetime_string_delta_eight = self.conver_datetime_sting_to_timestamp_sting(tag_name)

                if tag_name in self.all_framge_image_info_dict:

                    for second_dictor_name in self.all_framge_image_info_dict[tag_name]:
                        for third_director_name in self.all_framge_image_info_dict[tag_name][second_dictor_name]:
                            for frame_image_name in self.all_framge_image_info_dict[tag_name][second_dictor_name][third_director_name]:
                                if self.validate_second_range_before_and_after(check_target_image_timestamp_string,frame_image_name,2):
                                #if check_target_image_timestamp_string in frame_image_name:
                                    if os.path.exists(os.path.join(self.save_target_image_path,tag_name,second_dictor_name,third_director_name)):
                                        pass
                                    else:
                                        try:
                                            os.makedirs(os.path.join(self.save_target_image_path,tag_name,second_dictor_name,third_director_name))
                                        except Exception as e:
                                            print(e)

                                    # 由于不同的图像存储路径分隔符，导致图片无法查询到，此时要做特殊处理
                                    origin_image_path = os.path.join(self.image_frame_path,tag_name,second_dictor_name,third_director_name,frame_image_name)
                                    if not self.check_and_change_image_save_farther_folder(origin_image_path):
                                        # 图像帧存储父目录做特殊处理
                                        origin_image_path = os.path.join(self.image_frame_path,tag_name.replace("-","_"),second_dictor_name,third_director_name,frame_image_name)
                                    save_image_path = os.path.join(self.save_target_image_path,tag_name,second_dictor_name,third_director_name,frame_image_name)
                                    # print(origin_image_path)
                                    # print(save_image_path)
                                    # 将图片拷贝出来
                                    # shutil.copy(origin_image_path,save_image_path) #将图片拷贝出来
                                    print(tag_name,frame_image_name)
                                    snap_image_save_path_txt_row = os.path.join(tag_name,second_dictor_name,third_director_name,frame_image_name)
                                    if os.path.exists(os.path.join(self.save_target_image_path,snap_image_save_path_txt_row)):
                                        snap_image_save_path_txt_cur.write(snap_image_save_path_txt_row+'\n')
                                    else:
                                        print("the snap image : %s is not exists",snap_image_save_path_txt_row)
                                    self.total_copy_image_number+=1

                else:
                    print(tag_name)
                    continue
        snap_image_save_path_txt_cur.close()


target_file_path = "/data/save_cloud_camera_bag_video/animal/A3_tag_file"
image_frame_path = "/data/save_cloud_camera_bag_video/animal/A3_H265"
save_target_image_path = "/data/save_cloud_camera_bag_video/animal/A3_snap"
snap_image_save_path_txt = "/data/save_cloud_camera_bag_video/animal/A3_snap_save_path.txt"

get_target_image = UseTagInfoGetTargetImage(target_file_path,image_frame_path,save_target_image_path,snap_image_save_path_txt)
get_target_image.get_frame_image_info()
get_target_image.from_tag_dict_info_check_target_image()

print("the total copy target image number is :",get_target_image.total_copy_image_number)
# for tag_key in get_target_image.all_tag_info_dict.keys():
#     if "2023-12-28" in tag_key:
#         print(tag_key)
#
# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# for frame_image_key in get_target_image.all_framge_image_info_dict.keys():
#     if "2023_12_28" in frame_image_key:
#         print(frame_image_key)