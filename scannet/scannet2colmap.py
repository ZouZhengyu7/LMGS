import os
import shutil
from natsort import natsorted
import numpy as np
from scipy.spatial.transform import Rotation as R
blender2opencv = np.array([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
data_folder = 'scans/scene0062_00'
pose_folder = os.path.join(data_folder, "pose")
color_folder = os.path.join(data_folder, "color")
image_folder = os.path.join(data_folder, "images")
spare_folder = os.path.join(data_folder, "sparse")
if not os.path.exists(spare_folder):
    os.makedirs(spare_folder)
output_file = os.path.join(spare_folder, "images.txt")
cameras_file = os.path.join(spare_folder, "cameras.txt")
points3D_file = os.path.join(spare_folder, "points3D.txt")
with open(points3D_file, 'w') as f:
    pass
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
color_file = os.path.join(data_folder, 'intrinsic', "intrinsic_color.txt")
matrix = []
with open(color_file, 'r') as f:
    for line in f:
        matrix.append([float(x) for x in line.split()])
matrix = np.array(matrix)
fx = matrix[0, 0]
fy = matrix[1, 1]
cx = matrix[0, 2]
cy = matrix[1, 2]
camera_info = f"1 PINHOLE 1296 968 {fx} {fy} {cx} {cy}\n"
with open(cameras_file, 'w') as f:
    f.write(camera_info)
pose_file_list = [f for f in os.listdir(pose_folder) if f.endswith(".txt")]
# pose_file_list.sort()
pose_file_list=natsorted(pose_file_list,key=lambda x: int(os.path.splitext(x)[0]))
idx = 1
with open(output_file, 'w') as outfile:
    for filename in pose_file_list:
        file_path = os.path.join(pose_folder, filename)
        file_id = int(os.path.splitext(filename)[0])
        if file_id % 7 == 0:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                matrix = []
                for line in lines:
                    matrix.append(list(map(float, line.strip().split())))
                pose_matrix = np.array(matrix)
                q = np.linalg.inv(pose_matrix[:3, :3])
                translation = -np.matmul(q, pose_matrix[:3, 3])
                rotation = R.from_matrix(q)
                quaternion = rotation.as_quat()
            jpg_filename = f"{file_id}.jpg"
            jpg_file_path = os.path.join(color_folder, jpg_filename)
            if os.path.exists(jpg_file_path):
                dest_path = os.path.join(image_folder, jpg_filename)
                shutil.copy(jpg_file_path, dest_path)
                x, y, z, w = quaternion
                tx, ty, tz = translation
                outfile.write(f"{idx} {w} {x} {y} {z} {tx} {ty} {tz} 1 {jpg_filename}\n")
                outfile.write("\n")
                idx = idx + 1
