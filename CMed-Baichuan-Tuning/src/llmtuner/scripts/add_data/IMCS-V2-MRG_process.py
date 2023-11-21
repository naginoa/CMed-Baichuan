import json
import sys

import random

import difflib


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

import pandas as pd

input_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\IMCS-V2-MRG\IMCS-V2_train.json"
tarin_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\\train.json"
dev_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\dev.json"
test_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\Atest.json"
templates = "D:\load\pycharm\workplace\PromptCBLUE-main\src\data\\templates_augment.json"
output_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\process\process_IMCS-V2-MRG.json"
# task_dataset_dic=[]
# task_dataset_dic1 = []
list1=[]
list_train=[]

with open(tarin_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="IMCS-V2-MRG"):
            list_train.append(json_line["input"])

with open(dev_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="IMCS-V2-MRG"):
            list_train.append(json_line["input"])
with open(test_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="IMCS-V2-MRG"):
            list_train.append(json_line["input"])
with open(templates, 'r', encoding='utf-8') as f:
    templates= json.load(f)
    templates["IMCS-V2-MRG"]

import re

with open(input_dir, 'r', encoding='utf-8') as f:
    cdn_dic=json.load(f)
    for key,y in cdn_dic.items():
        # loads()：用于处理内的json对象，strip去除可能存在的空格
        text_line="患者："
        self_report=y["self_report"]
        report=y["report"]
        text_line+=self_report+"\n"
        dialogue=y["dialogue"]
        flag = 0
        for i in range(len(list_train)):
            if self_report in list_train[i]:
                print(self_report + "\n")
                flag = 1
        if flag == 0:
            for dia in dialogue:
                speaker=dia["speaker"]
                sentence=dia["sentence"]
                text_line+=speaker+"："
                text_line+=sentence+"\n"

            r1=random.randint(1,2)
            print(r1)
            for c in range(r1):
                r2=random.randint(1,2)
                for c1 in range(r2):
                    txt_json={}
                    output="上述问诊对话的诊疗报告如下：\n主诉：[1]\n现病史：[2]\n辅助检查：[3]\n既往史：[4]\n诊断：[5]\n建议：[6]"
                    output=output.replace("[1]",report[c1]["主诉"])
                    output=output.replace("[2]",report[c1]["现病史"])
                    output=output.replace("[3]", report[c1]["辅助检查"])
                    output=output.replace("[4]", report[c1]["既往史"])
                    output=output.replace("[5]", report[c1]["诊断"])
                    output=output.replace("[6]", report[c1]["建议"])


                    slice = random.randint(0, len(templates["IMCS-V2-MRG"]) - 1)
                    input_ = templates["IMCS-V2-MRG"][slice]
                    input_ = input_.replace("[INPUT_TEXT]", text_line[:-1:])
                    txt_json["input"] = input_
                    txt_json["target"]=output
                    # txt_json["answer_choices"] = labels_list
                    txt_json["task_type"] = "report_generation"
                    txt_json["task_dataset"] = "IMCS-V2-MRG"
                    txt_json["sample_id"] = "0"
                    list1.append(txt_json)
            # print(txt_json)
            # exit()
            print(len(list1))
            # if(len(list1)==1000):
            #     break
            # print("\n具有化疗关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为化疗。头实体为脉络丛乳头状癌，尾实体为术前化疗。\n具有预后生存率关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为5年生存率75%。头实体为脉络丛乳头状癌，尾实体为10年生存率66. 6%。\n具有手术治疗关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为手术全切。")
            # print(input_)
            # task_dataset=json_line["task_dataset"]
            # task_dataset_dic.append(task_dataset)
# list1=list1[:600:]
random.shuffle(list1)
print(len(list1))
with open(output_dir, 'w', encoding='utf-8') as write_f:
    count=0
    for i in range(600):
        write_f.write(json.dumps(list1[i], ensure_ascii=False))
        write_f.write('\n')
