import torch
import os
p = '/mnt/afs/zhangzhuo/experiments/had/unimodel/cross_rear/v1.18.a/ckpt_e30.pth'
model = torch.load(p, map_location='cpu')
vdc_task = ['rm','tsr','tlr','lightspot','obstacle']
had_front_task = ['rm', 'tsr', 'tlr', 'pole', 'obstacle', 'animal']
had_rear_task = ['rm_rear', 'pole']
m = model['model']
#modeldir = '/mnt/afs/guihao/pretrainedmodel/had/rear/20240329_2task_1anchor_HAD'
modeldir = '/mnt/afs/zhangzhuo/pretrainedmodel/had/rear/20240927_v1.18.a'
os.makedirs(modeldir,exist_ok=True)
os.system(f'cp {p} {modeldir}/')
for t in had_rear_task:
    taskmodel = {}
    for kt, kv in m.items():
        if 'cls' not in kt:
            taskmodel[kt] = m[kt]
        elif f'{t}_cls' in kt:
            taskmodel[kt.replace(f'{t}_','')] = m[kt]
    mm = {'model':taskmodel}
    torch.save(mm,os.path.join(modeldir,f'{t}.pth'))