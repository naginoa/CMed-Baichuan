import json
import sys

import random

import difflib


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

import pandas as pd

input_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\CHIP-CDN\CHIP-CDN_train.json"
tarin_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\\train.json"
dev_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\dev.json"
test_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\Atest.json"
templates = "D:\load\pycharm\workplace\PromptCBLUE-main\src\data\\templates_augment.json"
output_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\process\process_CHIP-CDN.json"
# task_dataset_dic=[]
# task_dataset_dic1 = []
list1=[]
list_train=[]

with open(tarin_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="CHIP-CDN"):
            list_train.append(json_line["input"])

with open(dev_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="CHIP-CDN"):
            list_train.append(json_line["input"])
with open(test_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="CHIP-CDN"):
            list_train.append(json_line["input"])
with open(templates, 'r', encoding='utf-8') as f:
    templates= json.load(f)
    templates["CHIP-CDN"]

import re

with open(input_dir, 'r', encoding='utf-8') as f:
    cdn_list=json.load(f)
    for json_line in cdn_list:
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        text=json_line["text"]
        flag = 0
        for i in range(len(list_train)):
            if text in list_train[i] or re.findall("[,.;:?，。；：？]",text):
                print(text+"\n")
                flag=1
                break
        if flag==0:
            path = 'D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\CHIP-CDN\ic10.xlsx'
            data = pd.DataFrame(pd.read_excel(path))  # 读取数据,设置None可以生成一个字典，字典中的key值即为sheet名字，此时不用使用DataFram，会报错
            scores_dic = {}
            for item in data["霍乱"]:
                scores_dic[item] = string_similar(text, item)
            scores_list = sorted(scores_dic.items(), key=lambda x: x[1], reverse=True)
            ran = random.randint(25, 30)
            # print(type(scores_list[:ran:]))
            labels_list = [item[0] for item in scores_list[:ran:]]
            # print(len(labels_list))
            normalized_result=json_line["normalized_result"]
            normalized_list=normalized_result.split("##")
            for i in normalized_list:
                if i not in labels_list:
                    ran = random.randint(0, len(labels_list) - 1)
                    labels_list.insert(ran, i)
            labels = "，".join(labels_list)
            # print(len(labels_list))
            slice = random.randint(0,len(templates["CHIP-CDN"])-1)
            input_=templates["CHIP-CDN"][slice]
            input_=input_.replace("[INPUT_TEXT]",text)
            input_ = input_.replace("[LIST_LABELS]", labels)

            output="，".join(normalized_list)

            txt_json={}
            txt_json["input"]=input_
            txt_json["target"]=output
            # txt_json["answer_choices"] = labels_list
            txt_json["task_type"] = "normalization"
            txt_json["task_dataset"] = "CHIP-CDN"
            txt_json["sample_id"] = "0"
            list1.append(txt_json)
            # print(input_)
            # print(txt_json)
            # exit()
            print(len(list1))
            if(len(list1)==1000):
                break
        # print("\n具有化疗关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为化疗。头实体为脉络丛乳头状癌，尾实体为术前化疗。\n具有预后生存率关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为5年生存率75%。头实体为脉络丛乳头状癌，尾实体为10年生存率66. 6%。\n具有手术治疗关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为手术全切。")
        # print(input_)
        # task_dataset=json_line["task_dataset"]
        # task_dataset_dic.append(task_dataset)

# with open(output_dir, 'w', encoding='utf-8') as write_f:
#     count=0
#     for i in range(len(list1)):
#         write_f.write(json.dumps(list1[i], ensure_ascii=False))
#         write_f.write('\n')
