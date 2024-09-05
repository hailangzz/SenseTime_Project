#!/usr/bin/env bash
# set -x

###############################################################################
#                        Configure Path and Info                              #
###############################################################################

T=`date +%m%d-%H%M`
DATE=`date +%m%d`
PLUGINPATH=/mnt/afs/guihao/project/up/up_plugin/rs
UPROOT=/mnt/up-lsl
VERSION=20240819_v1.18.a

CONFIG=/mnt/afs/guihao/experiment/deploy/FAW/HAD/front/uni_front.yaml
INPUT_SIZE=3x576x1024

WORKSPACE_ID=dae321d8-f409-439a-9c5b-ed44038ecc0e
PARTITION_ID=e5d9ee12-0053-4d12-8771-fb9d7eacd5da
RESOURCE_NAME=N1lS.Ia.I20.1
NODE=1

current_path=$(pwd)/${VERSION}/${INPUT_SIZE}
echo "当前路径是: $current_path"
mkdir -p $current_path
srun \
-j TOCAFFE \
-p $PARTITION_ID \
--workspace-id $WORKSPACE_ID \
-r $RESOURCE_NAME \
-f pytorch \
-m \
-N $NODE \
--container-image registry.st-sh-01.sensecore.cn/ad_semantics2d_ccr/roadsemantics-up:s0.3.4_cu102_ofed5.8 \
bash -c " \
cd $current_path
source s0.3.4 && \
export PYTHONPATH=$UPROOT:$PYTHONPATH && \
export PLUGINPATH=$PLUGINPATH && \
export EXCLUDE_TASKS=det_3d:action && \
python -m up to_caffe \
--config=$CONFIG \
--save_prefix=unimodel \
--input_size=$INPUT_SIZE"