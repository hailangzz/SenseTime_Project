import os

import torch


#p = '/data/model_deploy_folder/pretrain_model/unimodel/cross_front/v1.18.a/checkpoints/ckpt_e13.pth'
p = '/data/model_deploy_folder/pretrain_model/ckpt_e1.pth'
model = torch.load(p, map_location='cpu')
vdc_task = ['rm','tsr','tlr','lightspot','obstacle']
had_front_task = ['rm', 'tsr', 'tlr', 'pole', 'obstacle', 'animal']
had_rear_task = ['rm_rear', 'pole']

project=had_front_task

m = model['model']
modeldir = '/data/model_deploy_folder/pretrain_model/had/front/20240819_v1.18.a'

os.makedirs(modeldir,exist_ok=True)

os.system(f'cp {p} {modeldir}/')

for t in project:
    taskmodel = {}
    for kt, kv in m.items():
        if 'backbone' in kt or 'neck' in kt:
            taskmodel[kt] = m[kt]
        elif f'{t}' in kt:
            taskmodel[kt.replace(f'{t}_','')] = m[kt]
    mm = {'model':taskmodel}
    torch.save(mm,os.path.join(modeldir,f'{t}.pth'))
    print(f'{t}.pth done')