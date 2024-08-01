import json
import yaml
import copy

class CreatHadTagMapping:

    def __init__(self):
        self.statistics_tag_info_dict_path = "/home/SENSETIME/zhangzhuo/PycharmProjects/SenseTimePycharmProjects/获取DataSenseAuto上打过tag的泛化真值image数据信息/GetImageAwsSavePathFromDataSenseAuto/statistics_tag_info_dict.json"
        self.tag_statistics_info_dict = {}
        self.single_mapping_dict = {"name":"name",
                                    "id":0,
                                    "attribute":"attribute"}

        self.mapping_tag_dict={"mode":"one","mapping":[]}
    # 读取statistics_tag_info_dict.json文件
    def read_statistics_tag_info(self):
        with open(self.statistics_tag_info_dict_path,"r") as json_file:
            tag_info = json.load(json_file)
        self.tag_statistics_info_dict = tag_info["tag_statistics_info"]

    def save_mapping_tag_info(self):
        for index, (key, value) in enumerate(self.tag_statistics_info_dict.items()):
            print(f"{index}: {key} => {value}")
            self.single_mapping_dict['name'] = key
            self.single_mapping_dict['id'] = index
            self.single_mapping_dict['attribute'] = key
            self.mapping_tag_dict["mapping"].append(copy.deepcopy(self.single_mapping_dict))

        # 保存数据到 YAML 文件
        with open('./HadTagMapping_cls25.yml', 'w') as file:
            yaml.dump(self.mapping_tag_dict, file, allow_unicode=True, default_flow_style=False)


create_had_tag_mapping = CreatHadTagMapping()
create_had_tag_mapping.read_statistics_tag_info()
print(create_had_tag_mapping.tag_statistics_info_dict)
create_had_tag_mapping.save_mapping_tag_info()


    # # 读取 YAML 文件
    # with open('/home/SENSETIME/zhangzhuo/WorkSpace_SenseTime/dataxpert/datax/configs/sensebee/animal_cls4.yml', 'r') as file:
    #     config = yaml.safe_load(file)
    # # 输出读取到的数据
    # print(config)
    #
    # for key in config:
    #     print(key,config[key])
    #
    #
    # print("!!!!!!!!!!!!")
    # for key,values in config.items():
    #     print("key:%s" % key,"values:%s" % values)
    #
    # # 枚举输出字典数据
    # for index, (key, value) in enumerate(config.items()):
    #     print(f"{index}: {key} => {value}")