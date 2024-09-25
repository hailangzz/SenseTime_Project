import ffmpeg
import subprocess

def call_bash_script(script_path, file_path):
    try:
        # Call the bash script with the video file path as an argument
        result = subprocess.run(
            [script_path, file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Get the output and error from the result
        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode != 0:
            raise Exception(f"Error: {error}")

        return output

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_video_info(video_path):
    try:
        # 获取视频的流信息
        probe = ffmpeg.probe(video_path)
        video_info = None

        # 遍历流信息以找到视频流
        for stream in probe['streams']:
            if stream['codec_type'] == 'video':
                video_info = stream
                break

        if video_info is None:
            raise ValueError("没有找到视频流信息")

        # 提取所需的信息
        codec_name = video_info.get('codec_name', '未知')
        width = video_info.get('width', '未知')
        height = video_info.get('height', '未知')
        frame_rate = eval(video_info.get('r_frame_rate', '0/1'))
        bit_rate = int(video_info.get('bit_rate', 0))

        print(f"编码: {codec_name}")
        print(f"分辨率: {width}x{height}")
        print(f"帧率: {frame_rate:.2f} fps")
        # print(f"码率: {bit_rate / 1000} kbps")

    except ffmpeg.Error as e:
        print(f"ffmpeg错误: {e.stderr.decode('utf8')}")
    except Exception as e:
        print(f"发生错误: {e}")


# 替换为你的视频文件路径
video_path = '/home/SENSETIME/zhangzhuo/ws/issue_playback_data_folder/0830_date/2024_07_28_10_15_09/sensors_record/camera/center_camera_fov30.h265'

video_path_list = [
                    "/data/save_video_buffer/2024_06_18_10_40_10/sensors_record/camera/center_camera_fov120.h265",
                    "/data/save_video_buffer/2024_08_01_10_24_12_AutoCollect_2v78/sensors_record/camera/center_camera_fov120.h265",
                    "/data/save_video_buffer/2024_08_07_18_12_58_AutoCollect_2v78/sensors_record/camera/center_camera_fov120.h265",
                    "/data/save_video_buffer/2024_08_01_10_24_06_AutoCollect_202-5/sensors_record/camera/center_camera_fov120.h265",
                    "/data/save_video_buffer/2024_08_07_09_48_27_AutoCollect_202-5/sensors_record/camera/center_camera_fov120.h265",
                    "/data/save_video_buffer/2024_09_11_11_21_37_AutoCollect/sensors_record/camera/center_camera_fov30.h265",

                    "/data/save_video_buffer/2024_09_12_13_54_06_AutoCollect_2V78/sensors_record/camera/center_camera_fov120.h265",
                    "/data/save_video_buffer/2024_09_12_13_54_06_AutoCollect_2V78/sensors_record/camera/center_camera_fov120.h265",
                    "/data/save_video_buffer/2024_09_12_11_36_38_AutoCollect_2V56/sensors_record/camera/center_camera_fov120.h265",
                    "/data/save_video_buffer/2024_09_12_11_36_38_AutoCollect_2V56/sensors_record/camera/center_camera_fov120.h265"
                   ]
# Define the path to the bash script and the video file
script_path = '/data/save_video_buffer/video_rate.sh'

if __name__ == "__main__":
    # get_video_info(video_path)                         #获取视频其他信息
    for video_path in video_path_list:
        print("视频路径：{}".format(video_path))
        get_video_info(video_path)
        output = call_bash_script(script_path, video_path) #获取视频码率
        if output:
            print(output)