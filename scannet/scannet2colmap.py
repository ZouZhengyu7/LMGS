import shutil
import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation as R
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="Generate PLY file from data folder")
    parser.add_argument('--data_folder', type=str, required=True, help="Path to the data folder")
    args = parser.parse_args()
    data_folder = args.data_folder
    pose_folder = os.path.join(data_folder, "pose")
    color_folder = os.path.join(data_folder, "color")
    save_folder = str(os.path.join(os.path.dirname(os.path.dirname(args.data_folder)), os.path.basename(data_folder)))
    image_folder = os.path.join(save_folder, "images")
    input_folder = os.path.join(save_folder, "input")
    output_folder = os.path.join(save_folder, "output",str(os.path.basename(data_folder)))
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    spare_folder = os.path.join(save_folder, "sparse", "0")
    if not os.path.exists(spare_folder):
        os.makedirs(spare_folder)
    output_file = os.path.join(spare_folder, "images.txt")
    cameras_file = os.path.join(spare_folder, "cameras.txt")
    points3D_file = os.path.join(spare_folder, "points3D.txt")
    ply_file = os.path.join(data_folder, f"{os.path.basename(data_folder)}_vh_clean_2.ply")
    point_cloud = o3d.io.read_point_cloud(ply_file)
    points = np.asarray(point_cloud.points)
    if point_cloud.has_colors():
        colors = (np.asarray(point_cloud.colors) * 255).astype(np.uint8)
    else:
        colors = np.zeros_like(points)
    with open(points3D_file, 'w') as f:
        for idx, (point, color) in enumerate(zip(points, colors), start=1):
            f.write(f"{idx} {point[0]} {point[1]} {point[2]} {color[0]} {color[1]} {color[2]} 0\n")
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
    pose_file_list.sort(key=lambda x: int(os.path.splitext(x)[0]))
    idx = 1
    with open(output_file, 'w') as outfile:
        for filename in pose_file_list:
            file_path = os.path.join(pose_folder, filename)
            file_id = int(os.path.splitext(filename)[0])
            if file_id % 10 == 0:
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
                    dest_input_path = os.path.join(input_folder, jpg_filename)
                    shutil.copy(jpg_file_path, dest_path)
                    shutil.copy(jpg_file_path, dest_input_path)
                    x, y, z, w = quaternion
                    tx, ty, tz = translation
                    outfile.write(f"{idx} {w} {x} {y} {z} {tx} {ty} {tz} 1 {jpg_filename}\n")
                    outfile.write("\n")
                    idx = idx + 1


if __name__ == "__main__":
    main()
