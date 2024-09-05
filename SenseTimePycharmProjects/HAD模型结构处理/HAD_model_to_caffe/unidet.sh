# 输出路径
DATE=`date +%Y%m%d`
#DATE = "20240819"
VERSION=${DATE}_v1.18.a
mkdir -p $VERSION
OUT=${VERSION}/unidet.pth

# 配置torch模型路径
ROOT=/data/model_deploy_folder/pretrain_model/had/front
BASE=${ROOT}/tsr.pth
TSR=${ROOT}/${VERSION}/tsr_deploy_cls74.pth
TLR=${ROOT}/${VERSION}/tlr.pth
RM=${ROOT}/${VERSION}/rm.pth
POLE=${ROOT}/${VERSION}/pole.pth
ANIMAL=${ROOT}/${VERSION}/animal.pth
OBSTACLE=${ROOT}/${VERSION}/obstacle.pth

deployx model merge -b $TSR \
-a tlr=${TLR} \
-a tsr=${TSR} \
-a pole=${POLE} \
-a roadmarker=${RM} \
-a obstacle=${OBSTACLE} \
-a animal=${ANIMAL} \
-o ${OUT}
