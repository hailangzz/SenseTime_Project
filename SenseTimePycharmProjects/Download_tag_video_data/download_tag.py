from logging import exception
import os
import subprocess  

tags_dir = '/home/SENSETIME/zhangzhuo/PycharmProjects/SenseTimePycharmProjects/Download_tag_video_data/donwload_tag_txt_folder/animal/A3'
download_dir = '/data/save_cloud_camera_bag_video/animal/A3'

tag2data = {
    # '2023-12-11': 's3://sdc_gac/广州建图采集/2d量产版本采集/2023_12/segment_data/GOP/A02-459/20231211/', # 已下载_批次1
    # '2023-12-12': 's3://sdc_gac/广州建图采集/2d量产版本采集/2023_12/segment_data/GOP/A02-459/20231212/', # 已下载_批次1
    # '2023-12-14': 's3://sdc_gac/广州建图采集/2d量产版本采集/2023_12/segment_data/GOP/A02-459/20231214/', # 已下载_批次1
    # '2023-12-15': 's3://sdc_gac/广州建图采集/2d量产版本采集/2023_12/segment_data/GOP/A02-459/20231215/', # 已下载_批次1
    # '2023-12-16': 's3://sdc_gac/广州建图采集/2d量产版本采集/2023_12/segment_data/GOP/A02-459/20231216/', # 已下载_批次1
    # '2023-12-17': 's3://sdc_gac/广州建图采集/2d量产版本采集/2023_12/segment_data/GOP/A02-459/20231217/', # 已下载_批次1
    # '2023-12-18': 's3://sdc_gac/广州建图采集/2d量产版本采集/2023_12/segment_data/GOP/A02-459/20231218/', # 已下载_批次1
    # '2023-12-19': 's3://sdc_gac/广州建图采集/2d量产版本采集/2023_12/segment_data/GOP/A02-459/20231219/', # 已下载_批次1
    '2023-12-27': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/user_define/2023-12/A02-459/2023-12-27/',
    '2023-12-28': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/user_define/2023-12/A02-459/2023-12-28/',
    '2024-01-04': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/user_define/2023-12/A02-459/2024-01-04/',

    '2023-12-20': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/user_define/2023-12/2023-12-20/',
    '2023-12-21': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/user_define/2023-12/2023-12-21/',
    '2023-12-22': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/user_define/2023-12/2023-12-22/',
    '2023-12-23': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/user_define/2023-12/2023-12-23/',
    '2023-12-24': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/user_define/2023-12/2023-12-24/',
    '2023-12-25': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/user_define/2023-12/2023-12-25/',
    '2023-12-26': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/user_define/2023-12/2023-12-26/',
    '2024-01-19': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/GOP_gt/2024-01/A02-028/2024-01-19/',
    '2024-01-20': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/GOP_gt/2024-01/A02-028/2024-01-20/',

    'g29_r': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/user_define/2024-01/A02-290/2024-01-31/',
    'g29_y': 's3://sdc_gac/Data_Collection/GT_data/gacGtSegment/drive_gt_collection/PVB_gt/2024-01/A02-290/2024-01-31/'
}

tags_filename = os.listdir(tags_dir)
tags_filename.sort()

for tag in tags_filename:
    tag_name = tag.split('.')[0]
    # print(tag_name)

    if (tag_name>='2023-12-20'):

        with open(os.path.join(tags_dir, tag)) as f:
                lines = f.readlines()

        for idx, line in enumerate(lines):
            cur_anno = line.strip()
            # print(idx,cur_anno)
            # if('TSLR' not in cur_anno and 'TLSR' not in cur_anno and '红绿灯' not in cur_anno): #进行tag 目标的筛选：此时如果目标不包含TSLR、TLSR、红绿灯则不下载此录像数据
            #     continue
            if ('动物' not in cur_anno):  # 进行tag 目标的筛选：此时如果目标不包含TSLR、TLSR、红绿灯则不下载此录像数据
                continue
            else:
                print(idx, cur_anno)
            if(tag_name not in tag2data):
                # print(tag_name)
                continue
            timestamp = cur_anno.split(',')[0]
            # timestamp = timestamp.replace('-', '_')
            # timestamp = timestamp.replace(' ', '_')
            # timestamp = timestamp.replace(':', '_')
            # print("tag_name:  ",tag_name)
            if(tag_name in ('2023-12-11','2023-12-12','2023-12-14','2023-12-15','2023-12-16','2023-12-17','2023-12-18','2023-12-19')):
                timestamp = timestamp.replace('-', '-')
                timestamp = timestamp.replace(' ', '-')
                timestamp = timestamp.replace(':', '-')
            else:
                timestamp = timestamp.replace('-', '_')
                timestamp = timestamp.replace(' ', '_')
                timestamp = timestamp.replace(':', '_')

            source_path = os.path.join(tag2data[tag_name], timestamp)
            target_path = os.path.join(download_dir, tag_name, timestamp)
            # print(source_path)
            try:
                # 输出当天不同时段的桶文件名称：
                cmd = [
                    'aws',
                    '--endpoint-url=http://sdc-oss.iagproxy.senseauto.com',
                    '--profile', 'ad_system_common',
                    's3', 'ls', tag2data[tag_name] ,
                ]
                # print(cmd)
                files = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                director_out_str = files.stdout
                director_out_name_list = director_out_str.split('\n')

                for director_name in director_out_name_list:
                    # print(timestamp)
                    if('-' in timestamp):
                        timestamp_split_list = timestamp.split('-')
                        timestamp_split_list[3] = str(int(timestamp_split_list[3]) + 8)
                        timestamp_add_eight_hours = '-'.join(timestamp_split_list)
                    elif('_' in timestamp):

                        timestamp_split_list = timestamp.split('_',)
                        timestamp_split_list[3] = str(int(timestamp_split_list[3]) + 8)
                        timestamp_add_eight_hours = '_'.join(timestamp_split_list)
                    # print(timestamp,'timestamp_add_eight_hours:',timestamp_add_eight_hours)
                    #
                    # print(director_name)
                    if (timestamp in director_name):    # 当tag时间戳包含在桶目录名称中时，直接抽取bag包
                        cmd = [
                            'aws',
                            '--endpoint-url=http://sdc-oss.iagproxy.senseauto.com',
                            '--profile', 'ad_system_common',
                            's3', 'ls', source_path+'/',
                            ]
                    elif(timestamp_add_eight_hours in director_name):
                        cmd = [
                            'aws',
                            '--endpoint-url=http://sdc-oss.iagproxy.senseauto.com',
                            '--profile', 'ad_system_common',
                            's3', 'ls', os.path.join(tag2data[tag_name], timestamp_add_eight_hours) + '/',
                        ]
                    else:
                        continue

                    # print(cmd)
                    files = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    out_str = files.stdout
                    outs = out_str.split('\n')
                    # print(len(out_str))
                    # print(outs)
                    for out in outs:
                        if('01-CameraRadarLidar' in out):
                            camera_ladar_str = out
                            break
                    camera_ladar_file = camera_ladar_str.split('\n')[0].split(' ')[-1]

                    # print(timestamp)
                    #camera_ladar_file ="01-CameraRadarLidar_"+timestamp+".bag"
                    # camera_ladar_file = "01-CameraRadarLidar_" + "*.bag"

                    if (timestamp_add_eight_hours in director_name):    # 当tag时间戳包含在桶目录名称中时，直接抽取bag包
                        source_path = os.path.join(tag2data[tag_name], timestamp_add_eight_hours)
                    source_path = os.path.join(source_path, camera_ladar_file)
                    target_path = os.path.join(target_path, camera_ladar_file)

                    cmd = [
                        'aws',
                        '--endpoint-url=http://sdc-oss.iagproxy.senseauto.com',
                        '--profile', 'ad_system_common',
                        's3', 'cp', source_path, target_path,
                        ]
                    subprocess.run(cmd)
            except Exception as e:
                print(e)
                print(tag_name)
