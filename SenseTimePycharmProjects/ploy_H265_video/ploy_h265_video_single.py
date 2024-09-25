import cv2
import os

#video_origin_path = "/data/save_video_buffer/2024_09_12_13_54_06_AutoCollect_2V78/sensors_record/camera"
video_origin_path = "/data/save_video_buffer/2024_09_12_11_36_38_AutoCollect_2V56/sensors_record/camera"


# 视频文件路径
video_path = os.path.join(video_origin_path,'center_camera_fov30.h265')

# 打开视频文件
cap = cv2.VideoCapture(video_path)

# 检查视频是否成功打开
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# 初始化播放状态
is_playing = True

# 播放视频
while True:
    if is_playing:
        ret, frame = cap.read()
        if not ret:
            break
        # 显示每一帧
        cv2.imshow('H.265 Video', frame)

    # 检测按键
    key = cv2.waitKey(25) & 0xFF
    if key == ord('q') or key == 27:  # 27 是 Esc 键的 ASCII 码
        break
    elif key == ord(' '):  # 空格键控制播放/暂停
        is_playing = not is_playing

# 释放视频捕捉对象并关闭所有窗口
cap.release()
cv2.destroyAllWindows()