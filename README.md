# Scannet

下载Scannet数据集(指定场景)，导出位姿和图片等，并转化为colmap的格式

```shell
cd scannet
#下载到scans或者scans_test目录
python download.py -o . --id scene0000_00
#导出位姿和图片等，Python2.7
python reader.py --filename scans/scene0000_00/scene0000_00.sens  --output_path scans/scene0000_00 --export_depth_images --export_color_images --export_poses --export_intrinsics
#转化为colmap的格式
python scannet2colmap.py --data_folder scans/scene0000_00
#此时scannet目录应为：scene0617_00为后面训练的输入,结构和langsplat的一致
├── download.py
├── reader.py
├── scannet2colmap.py
├── scans
│   └── scene0617_00
├── scene0617_00
│   └── images
│   └── input
│   └── output
│   └── sparse
├── SensorData.py
├── SensorData.pyc
```

# PGSR

要切换分支。。。。。。

```shell
cd ../PGSR
python train.py -s ../scannet/scene000_00 -m ../scannet/scene000_00/output/scene000_00 --max_abs_split_points 0 --opacity_cull_threshold 0.05
#渲染
python render.py -m ../scannet/scene000_00/output/scene000_00 --max_depth 5.0 --voxel_size 0.01
#计算指标 SSIM PSNR LPIPS
python metrics.py -m ../scannet/scene000_00/output/scene000_00 -g ../scannet/scene000_00/input
```

# LangSplat

修改一下process.sh中的base_path，比如"scannet/scene0000_00"

```shell
sh process.sh
```

