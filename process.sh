#!/bin/bash
base_path="scannet/scene0617_00_3dgs"
dataset_path=$base_path
dataset_name=$(basename $base_path)
casename=$(basename $base_path)
python preprocess.py --dataset_path $dataset_path

# train the autoencoder
# shellcheck disable=SC2164
cd autoencoder
python train.py --dataset_path ../$dataset_path --encoder_dims 256 128 64 32 3 --decoder_dims 16 32 64 128 256 256 512 --lr 0.0007 --dataset_name $dataset_name
# e.g. python train.py --dataset_path ../data/sofa --encoder_dims 256 128 64 32 3 --decoder_dims 16 32 64 128 256 256 512 --lr 0.0007 --dataset_name sofa

# get the 3-dims language feature of the scene
python test.py --dataset_path ../$dataset_path --dataset_name $dataset_name
# e.g. python test.py --dataset_path ../data/sofa --dataset_name sofa

# ATTENTION: Before you train the LangSplat, please follow https://github.com/graphdeco-inria/gaussian-splatting
# to train the RGB 3D Gaussian Splatting model.
# put the path of your RGB model after '--start_checkpoint'
cd ..
for level in 1 2 3
do
    python train.py -s $dataset_path -m output/${casename} --start_checkpoint $dataset_path/output/$dataset_name/chkpnt30000.pth --feature_level ${level} --port 44444
    # e.g. python train.py -s data/sofa -m output/sofa --start_checkpoint data/sofa/sofa/chkpnt30000.pth --feature_level 3
done

for level in 1 2 3
do
    # render rgb
    python render.py -m output/${casename}_${level}
    # render language features
    python render.py -m output/${casename}_${level} --include_feature
    # e.g. python render.py -m output/sofa_3 --include_feature
done