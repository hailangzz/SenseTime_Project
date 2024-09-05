import argparse
import os

import torch

# 此脚本主要是针对tsr模型，由于融合模型在输出类别上，有大概4类是不需要数据的，因此需要将融合模型中，切分下来的tsr模型中的对应4个输出channle移除
# 注意：这里使用model为融合模型切分后的tsr模型，且task参数使用tsr_dsp

# tsr deploy tocaffe classname
tsr_deployname = ["speed-5", "speed-10", "speed-15", "speed-20", "speed-25", "speed-30", "speed-35", "speed-40",
                  "speed-50", "speed-60", "speed-70",
                  "speed-80", "speed-90", "speed-100", "speed-110", "speed-120", "ElecSpeed",
                  "lift-5", "lift-10", "lift-15", "lift-20", "lift-25", "lift-30", "lift-35", "lift-40", "lift-50",
                  "lift-60", "lift-70", "lift-80",
                  "lift-90", "lift-100", "lift-110", "lift-120",
                  "Min_speed_50", "Min_speed_60", "Min_speed_70", "Min_speed_80", "Min_speed_90", "Min_speed_100",
                  "Min_speed_110",
                  "x-pass", "lift-pass", "x-height", "x-weight", "x-width", "stop", "slow-down", "x-parking", "x-enter",
                  "x-entry", "x-straight",
                  "x-left", "x-right", "x-left-right", "x-Uturn", "x-whistle",
                  "merge-left", "merge-right", "notice-ped", "notice-child", "lane-merge", "construction", "diversion",
                  "crosswalk",
                  "straight-lane", "uturn-lane", "turn-left", "turn-right", "left-straight-turn-lane",
                  "right-straight-turn-lane", "left-U-turn-lane",
                  "bus-lane", "high-speed-destination", "ramp", ]
# tsr training classname
tsr_trainingname = ["speed-5", "speed-10", "speed-15", "speed-20", "speed-25", "speed-30", "speed-35", "speed-40",
                    "speed-50", "speed-60", "speed-70",
                    "speed-80", "speed-90", "speed-100", "speed-110", "speed-120", "ElecSpeed",
                    "lift-5", "lift-10", "lift-15", "lift-20", "lift-25", "lift-30", "lift-35", "lift-40", "lift-50",
                    "lift-60", "lift-70", "lift-80",
                    "lift-90", "lift-100", "lift-110", "lift-120",
                    "Min_speed_50", "Min_speed_60", "Min_speed_70", "Min_speed_80", "Min_speed_90", "Min_speed_100",
                    "Min_speed_110",
                    "x-pass", "lift-pass", "x-height", "x-weight", "x-width", "stop", "slow-down", "x-parking",
                    "x-enter", "x-entry", "x-straight",
                    "x-left", "x-right", "x-left-right", "x-Uturn", "x-whistle",
                    "merge-left", "merge-right", "notice-ped", "notice-child", "lane-merge", "construction",
                    "diversion", "crosswalk",
                    "straight-lane", "uturn-lane", "turn-left", "turn-right", "left-straight-turn-lane",
                    "right-straight-turn-lane", "left-U-turn-lane",
                    "bus-lane", "high-speed-destination", "ramp", "lane-number", "slow", "speed-limit-sticker"]

tsr_trainingname_dsb = ["speed-5", "speed-10", "speed-15", "speed-20", "speed-25", "speed-30", "speed-35", "speed-40",
                        "speed-50", "speed-60", "speed-70",
                        "speed-80", "speed-90", "speed-100", "speed-110", "speed-120", "ElecSpeed",
                        "lift-5", "lift-10", "lift-15", "lift-20", "lift-25", "lift-30", "lift-35", "lift-40",
                        "lift-50", "lift-60", "lift-70", "lift-80",
                        "lift-90", "lift-100", "lift-110", "lift-120",
                        "Min_speed_50", "Min_speed_60", "Min_speed_70", "Min_speed_80", "Min_speed_90", "Min_speed_100",
                        "Min_speed_110",
                        "x-pass", "lift-pass", "x-height", "x-weight", "x-width", "stop", "slow-down", "x-parking",
                        "x-enter", "x-entry", "x-straight",
                        "x-left", "x-right", "x-left-right", "x-Uturn", "x-whistle",
                        "merge-left", "merge-right", "notice-ped", "notice-child", "lane-merge", "construction",
                        "diversion", "crosswalk",
                        "straight-lane", "uturn-lane", "turn-left", "turn-right", "left-straight-turn-lane",
                        "right-straight-turn-lane", "left-U-turn-lane",
                        "bus-lane", "high-speed-destination", "ramp", "lane-number", "slow", "speed-limit-sticker",
                        "digit-sign-block"]

# ls deploy tocaffe classname
ls_depolyname = ["HeadLight", "TailLight", "StreetLamp", "HeadPair", "TailPair"]
ls_depolyname3 = ["HeadLight", "TailLight", "StreetLamp"]
# ls training classname
ls_trainingname7 = ["HeadLight", "TailLight", "StreetLamp", "HeadPair", "TailPair", "BrakeLight", "RefectLight"]
ls_trainingname6 = ["HeadLight", "TailLight", "StreetLamp", "HeadPair", "TailPair", "BrakeLight"]

# tlr att deploy classname
tlr_depolyname = ["attention", "no_attention", "non_related"]

# tlr att training classname
tlr_trainingname = ["tlight", "attention", "no_attention", "non_related"]

taskinfo = {
    'tsr': {'trainName': tsr_trainingname, 'deployName': tsr_deployname},
    'tsr_dsb': {'trainName': tsr_trainingname_dsb, 'deployName': tsr_deployname},
    'ls7': {'trainName': ls_trainingname7, 'deployName': ls_depolyname},
    'ls6': {'trainName': ls_trainingname6, 'deployName': ls_depolyname},
    'ls6_d3': {'trainName': ls_trainingname6, 'deployName': ls_depolyname3},
    'tlr_at': {'trainName': tlr_trainingname, 'deployName': tlr_depolyname},
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='ls_cls6.pth', help='modelpath')
    parser.add_argument('--task', choices=['tsr', 'tsr_dsb', 'ls6', 'ls7', 'ls6_d3', 'tlr_at'], help='task name')
    # parser.add_argument('--anchor', type=int, default=1, help='anchor number')
    args = parser.parse_args()

    nowName = taskinfo[args.task]['trainName']
    oldName = taskinfo[args.task]['deployName']
    idx = [nowName.index(name) for name in oldName]
    print(f"idx===>{idx}")
    # anchor = args.anchor
    clsnums = len(nowName)

    model = torch.load(args.model, map_location='cpu')
    m = model['model']
    tensor = m['roi_head.cls_subnet_pred.weight']
    tensorb = m['roi_head.cls_subnet_pred.bias']
    if tensor.size()[0] % clsnums != 0:
        raise ValueError("模型输出数无法被类别数整除, 检查再检查")

    anchor = tensor.size()[0] // clsnums
    print(f"anchor===>{anchor}")
    model['model']['roi_head.cls_subnet_pred.weight'] = torch.cat(
        [tensor[i * clsnums:(i + 1) * clsnums][idx] for i in range(anchor)])
    model['model']['roi_head.cls_subnet_pred.bias'] = torch.cat(
        [tensorb[i * clsnums:(i + 1) * clsnums][idx] for i in range(anchor)])
    p, suffix = os.path.splitext(args.model)
    torch.save(model, f'{p}_deploy_cls{len(idx)}{suffix}')


if __name__ == '__main__':
    main()