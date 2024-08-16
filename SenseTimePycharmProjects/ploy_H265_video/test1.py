import subprocess
import json


def get_video_color_info(file_path):
    try:
        # Call ffprobe to get video color information
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'stream=color_space,color_transfer,color_primaries', '-of',
             'json', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        info = json.loads(result.stdout)

        # Extract video stream information
        video_streams = info.get('streams', [])
        if not video_streams:
            raise ValueError("No video stream found")

        video_info = video_streams[0]
        color_space = video_info.get('color_space')
        color_transfer = video_info.get('color_transfer')
        color_primaries = video_info.get('color_primaries')

        return {
            'color_space': color_space,
            'color_transfer': color_transfer,
            'color_primaries': color_primaries
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Define the path to the video file
video_file_path = '/path/to/your/video/file.mp4'

if __name__ == "__main__":
    info = get_video_color_info(video_file_path)
    if info:
        print(f"Color Space: {info['color_space']}")
        print(f"Color Transfer: {info['color_transfer']}")
        print(f"Color Primaries: {info['color_primaries']}")

# Define the path to the video file
video_file_path = "/home/SENSETIME/zhangzhuo/ws/issue_playback_data_folder/0830_date/2024_07_28_10_15_09/sensors_record/camera/center_camera_fov30.h265"

if __name__ == "__main__":
    info = get_video_color_info(video_file_path)
    if info:
        print(f"Color Space: {info['color_space']}")
        print(f"Color Transfer: {info['color_transfer']}")
        print(f"Color Primaries: {info['color_primaries']}")
