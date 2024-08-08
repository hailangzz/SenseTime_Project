import cv2
import numpy as np
import os

# 视频文件路径
# video_path_1 = '/data/save_video_buffer/2024_06_18_10_40_10/sensors_record/camera'
# video_path_2 = '/data/save_video_buffer/2024_07_11_18_29_56_AutoCollect/sensors_record/camera'

# video_path_1 = '/data/save_video_buffer/2024_07_11_18_29_56_AutoCollect/sensors_record/camera'
#video_path_2 = '/data/save_video_buffer/2024_07_11_18_29_56_AutoCollect/sensors_record/camera'
#video_path_2 = "/home/SENSETIME/zhangzhuo/.deepinwine/Deepin-WXWork/drive_c/users/zhangzhuo/Documents/WXWork/1688854535539608/Cache/File/2024-08/"
#白天摄像头视频效果对比
video_path_1 = '/data/save_video_buffer/2024_08_07_09_48_27_AutoCollect/sensors_record/camera'
# video_path_2 = "/home/SENSETIME/zhangzhuo/.deepinwine/Deepin-WXWork/dosdevices/c:/users/zhangzhuo/Documents/WXWork/1688854535539608/Cache/File/2024-08/daytime/"
video_path_2 = '/data/save_video_buffer/2024_08_01_10_24_06_AutoCollect/sensors_record/camera'
#
# video_path_left = os.path.join(video_path_1,"center_camera_fov30.h265")
# video_path_right = os.path.join(video_path_2,"center_camera_fov30.h265")

# #夜间摄像头视频效果对比
# video_path_1 = '/data/save_video_buffer/2024_08_01_10_24_06_AutoCollect/sensors_record/camera'
# video_path_2 = "/data/save_video_buffer/2024_08_01_10_24_12_AutoCollect/sensors_record/camera"

video_type_string = "fov120"  # 选择对比哪个摄像头的录像数据 fov30、fov120
video_path_left = os.path.join(video_path_1,"center_camera_{}.h265".format(video_type_string))
video_path_right = os.path.join(video_path_2,"center_camera_{}.h265".format(video_type_string))

# 打开视频文件
cap1 = cv2.VideoCapture(video_path_left)
cap2 = cv2.VideoCapture(video_path_right)


# 检查视频是否成功打开
if not cap1.isOpened():
    print("Error: Could not open the first video.")
    exit()
if not cap2.isOpened():
    print("Error: Could not open the second video.")
    exit()

# 获取视频的帧率和帧大小
fps = int(cap1.get(cv2.CAP_PROP_FPS))
frame_width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 初始化播放状态
is_playing = True

# 设置窗口大小
window_width = 1880
window_height = 829

# 设置视频保存路径和格式
output_path = 'night_video_compare_{}.mp4'.format(video_type_string)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 指定视频编码器
output = cv2.VideoWriter(output_path, fourcc, fps, (window_width, window_height))

# 计算保存视频的帧数限制
save_frame_limit = fps * 80  # 80秒的视频帧数限制

# 播放视频
frame_count = 0
while True:
    if is_playing:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            break

        # 调整帧大小以适应窗口的左右两半
        frame1 = cv2.resize(frame1, (window_width // 2, window_height))
        frame2 = cv2.resize(frame2, (window_width // 2, window_height))

        # 将两个视频帧拼接成一个窗口
        combined_frame = np.hstack((frame1, frame2))

        # 显示拼接后的帧
        cv2.imshow('H.265 Videos', combined_frame)

        # 保存前2分钟的视频帧
        if frame_count < save_frame_limit:
            output.write(combined_frame)
            frame_count += 1
        else:
            break

    # 检测按键
    key = cv2.waitKey(25) & 0xFF
    if key == ord('q') or key == 27:  # 27 是 Esc 键的 ASCII 码
        break
    elif key == ord(' '):  # 空格键控制播放/暂停
        is_playing = not is_playing

# 释放视频捕捉对象和视频写入对象并关闭所有窗口
cap1.release()
cap2.release()
output.release()
cv2.destroyAllWindows()
