import torch
import argparse
import math
# 此脚本的目的是，当客户增加了项目的输出类别时，为了保证原来的预训练模型能在增加目标分类输出后，仍然能正常的加载使用
# 因此才使用此脚本，为原来的模型增加对应类别的输出channle数，从而满足在增加模型输出后，在读取原有模型的参数信息时，仍然能进行多增加输出类别后的模型训练

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='ls_cls6.pth', help='modelpath')

    args = parser.parse_args()
    model = torch.load(args.model, map_location='cpu')
    m = model['model']
    tensor = m['roi_head.tsr_cls_subnet_pred.weight']
    tensorb = m['roi_head.tsr_cls_subnet_pred.bias']
    new_pred = torch.nn.Conv2d(24,78,kernel_size=3,stride=1,padding=1)
    for m_new in new_pred.modules():
        torch.nn.init.normal_(m_new.weight.data, std=0.01)
        m_new.bias.data.normal_(-math.log(1.0 / 0.01 - 1.0), 0.01)
        torch.nn.init.constant_(m_new.bias, -math.log(1.0 / 0.01 - 1.0))
    new_weight = m_new.state_dict()['weight']
    new_bias = m_new.state_dict()['bias']
    new_weight[:78] = tensor
    new_bias[:78] = tensorb
    m['roi_head.tsr_cls_subnet_pred.weight'] = new_weight
    m['roi_head.tsr_cls_subnet_pred.bias'] = new_bias
    torch.save(model, f'uni_dsb.pth')
        #m_new.bias.data.normal_()

if __name__ == '__main__':
    main()