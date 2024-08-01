bag_out_folder="/mnt/lustrenew/sunguodong/gac_fanhua_regular/0035/raw_data/"
OUTFOLDER="/mnt/lustrenew/sunguodong/gac_fanhua_regular/0035/frame_data/"

dir=$(ls -l ${bag_out_folder} |awk '/^d/ {print $NF}')

for i in $dir
do  
    sub_filename='/port_0_camera_0_front_fov30_instanceID_75.h265'
    hevc_path="${bag_out_folder}${i}${sub_filename}"
    out_png_sub_folder="${OUTFOLDER}${i}/port_0_camera_0_front_fov30_instanceID_75/"
    echo $out_mp4_folder
    
    if [ ! -d "$out_png_sub_folder" ]; then
        mkdir -p "$out_png_sub_folder"
    fi

    # out_mp4_name="${out_mp4_folder}center_camera_fov120.mp4"


    # ffmpeg -f hevc -i ${hevc_path} -vcodec copy ${out_mp4_name}
    ffmpeg -i $hevc_path -r 2 "${out_png_sub_folder}%08d.jpg"
    # nohup ffmpeg -i $hevc_path -r 2 "${out_png_sub_folder}%08d.jpg"  > /mnt/lustrenew/sunguodong/raw_data_process/nohup_out/0030_${i}_fov30 2>&1 &   

    sub_filename='/port_0_camera_2_front_fov120_instanceID_76.h265'
    hevc_path="${bag_out_folder}${i}${sub_filename}"
    out_png_sub_folder="${OUTFOLDER}${i}/port_0_camera_2_front_fov120_instanceID_76/"
    echo $out_mp4_folder
    
    if [ ! -d "$out_png_sub_folder" ]; then
        mkdir -p "$out_png_sub_folder"
    fi

    # out_mp4_name="${out_mp4_folder}center_camera_fov120.mp4"


    # ffmpeg -f hevc -i ${hevc_path} -vcodec copy ${out_mp4_name}
    # ffmpeg -i $hevc_path -r 2 "${out_png_sub_folder}%08d.jpg" # 2代表每秒解析2帧
    nohup ffmpeg -i $hevc_path -r 1 "${out_png_sub_folder}%08d.jpg" > /mnt/lustrenew/sunguodong/raw_data_process/nohup_out/0028_${i}_fov120 2>&1 &
done