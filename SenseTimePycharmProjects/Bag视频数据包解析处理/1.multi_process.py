import os  
import glob  
import subprocess  
  
def process_bag_file(bag_path, save_path_base):  
    save_path = os.path.join(save_path_base, os.path.basename(bag_path))   
    cmd = [  
        "/opt/bagKits/run_shell.sh",  
        "-i", bag_path,  
        "-o", save_path,  
        "-m", "camera",
        "-c", '"front_fov30","front_fov120"',
    ]  
    print(cmd)
    subprocess.run(cmd)  
  
def find_and_process_bag_files(base_dir, output_dir):
    # import pdb; pdb.set_trace()
    for root, dirs, files in os.walk(base_dir): 
        # import pdb; pdb.set_trace()
        for filename in files:  
            if filename.startswith("01-CameraRadarLidar"):

                process_bag_file(root, output_dir)

if __name__ == "__main__": 
    # import pdb; pdb.set_trace()
    base_dir = "/data/save_cloud_camera_bag_video/animal/A3/"
    output_dir = "/data/save_cloud_camera_bag_video/animal/A3_H265/"
    if(not os.path.exists(output_dir)):
        os.makedirs(output_dir)
    find_and_process_bag_files(base_dir, output_dir)
