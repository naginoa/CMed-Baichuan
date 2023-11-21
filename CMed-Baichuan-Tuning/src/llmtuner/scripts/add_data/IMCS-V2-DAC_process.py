import json
import sys

import random

import difflib


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

import pandas as pd

input_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\IMCS-V2-DAC\IMCS-V2_train.json"
tarin_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\\train.json"
dev_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\dev.json"
test_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\Atest.json"
templates = "D:\load\pycharm\workplace\PromptCBLUE-main\src\data\\templates_augment.json"
output_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\process\process_IMCS-V2-DAC.json"
# task_dataset_dic=[]
# task_dataset_dic1 = []
list1=[]
list_train=[]
answ_dic={}
with open(tarin_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="IMCS-V2-DAC"):
            list_train.append(json_line["input"])

'''
[('非上述类型', 1763), ('关于症状的回答', 667), ('关于症状的询问', 436), 
('关于用药建议的解答',  329), ('关于已有检查和治疗的回答', 291), ('关于个人基本信息的回答', 223), ('关于注意事项的解答', 222), 
('关于就医建议的解答', 201), ('关已有检查和治疗的提问', 188), ('关于用药建议的提问', 179), 
('关于个人基本信息的询问', 148), ('给出诊断', 126), ('关于病因的回答', 79), ('关于就医建议的提问', 58), 
('关于病因的询问', 48), ('关于注意事项的提问', 42)]

dict_keys(['关于注意事项的解答', '关于症状的询问', '关于已有检查和治疗的提问', '非上述类型', '关于个人基本信息的回答', 
'关于用药建议的解答', '关于症状的回答', '关于用药建议的提问', '关于已有检查和治疗的回答', '关于就医建议的解答', 
'关于个人基本信息的询问', '关于注意事项的提问', '给出诊断', '关于就医建议的提问', '关于病因的询问', '关于病因的回答'])

'''
dialogue_act_dic={"Inform-Precautions":'关于注意事项的解答', "Request-Symptom":'关于症状的询问',
    "Request-Existing_Examination_and_Treatment":'关于已有检查和治疗的提问', "Other":'非上述类型',
                  "Inform-Basic_Information":'关于个人基本信息的回答',
                    "Inform-Drug_Recommendation":'关于用药建议的解答',"Inform-Symptom":'关于症状的回答',
                                "Request-Drug_Recommendation":'关于用药建议的提问',
                    "Inform-Existing_Examination_and_Treatment":'关于已有检查和治疗的回答',
"Inform-Medical_Advice":'关于就医建议的解答',"Request-Basic_Information":'关于个人基本信息的询问',
                  "Request-Precautions":'关于注意事项的提问',"Diagnose": '给出诊断', "Request-Medical_Advice":'关于就医建议的提问',
"Request-Etiology":'关于病因的询问', "Inform-Etiology":'关于病因的回答'}
labels=['关于注意事项的解答', '关于症状的询问', '关于已有检查和治疗的提问', '非上述类型', '关于个人基本信息的回答',
'关于用药建议的解答', '关于症状的回答', '关于用药建议的提问', '关于已有检查和治疗的回答', '关于就医建议的解答',
'关于个人基本信息的询问', '关于注意事项的提问', '给出诊断', '关于就医建议的提问', '关于病因的询问', '关于病因的回答']
with open(dev_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="IMCS-V2-DAC"):
            list_train.append(json_line["input"])
with open(test_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="IMCS-V2-DAC"):
            list_train.append(json_line["input"])
with open(templates, 'r', encoding='utf-8') as f:
    templates= json.load(f)
    templates["IMCS-V2-DAC"]

import re

with open(input_dir, 'r', encoding='utf-8') as f:
    cdn_dic=json.load(f)
    for key,y in cdn_dic.items():
        # loads()：用于处理内的json对象，strip去除可能存在的空格
        text_line=""
        self_report=y["self_report"]
        report=y["report"]
        # text_line+=self_report+"\n"
        dialogue=y["dialogue"]
        flag = 0
        for i in range(len(list_train)):
            if self_report in list_train[i]:
                # print(self_report + "\n")
                flag = 1
        if flag == 0:
            ren = random.randint(1,5)
            for i in range(ren):
                st=random.randint(1,len(dialogue)//2)
                end=random.randint(st+2,len(dialogue)-1)
                print(dialogue[end-1]["dialogue_act"])
                tmp=dialogue[end - 1]["dialogue_act"]
                cc=0
                while tmp == "Other" or tmp == "Request-Symptom" or tmp == "Inform-Symptom":
                    st = random.randint(1, len(dialogue) // 2)
                    end = random.randint(st + 2, len(dialogue) - 1)
                    print(dialogue[end - 1]["dialogue_act"])
                    tmp = dialogue[end - 1]["dialogue_act"]
                    cc+=1
                    if cc==20:
                        break

                if tmp != "Other" and tmp != "Request-Symptom" and tmp != "Inform-Symptom":
                    print(st,end)
                    print(dialogue[end-1]["sentence"])
                    # exit()
                    for id in range(st,end):
                        dia=dialogue[id]
                        speaker=dia["speaker"]
                        sentence=dia["sentence"]
                        dialogue_act=dia["dialogue_act"]
                        text_line+=speaker+"："
                        text_line+=sentence+"\n"

                    txt_json={}
                    output=dialogue_act_dic[tmp]
                    slice = random.randint(0, len(templates["IMCS-V2-DAC"]) - 1)
                    input_ = templates["IMCS-V2-DAC"][slice]
                    input_ = input_.replace("[INPUT_TEXT]", text_line[:-1:])
                    ren = random.randint(8, 11)

                    # label=dialogue_act_dic[dialogue_act]
                    # if label not in labels_list:
                    #     ran = random.randint(0, len(labels_list) - 1)
                    #     labels_list.insert(ran, label)
                    # labels = "，".join(labels_list)

                    print(labels)
                    input_ = input_.replace("[LIST_LABELS]", "，".join(labels))
                    txt_json["input"] = input_
                    txt_json["target"]=output
                    # print(txt_json)
                    # exit()
                    txt_json["answer_choices"] = labels
                    txt_json["task_type"] = "cls"
                    txt_json["task_dataset"] = "IMCS-V2-DAC"
                    txt_json["sample_id"] = "0"
                    list1.append(txt_json)
                    # print(list1)
                    # exit()
                    # print(txt_json)
                    # exit()
                    # print(len(list1))
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
    for i in range(1000):
        write_f.write(json.dumps(list1[i], ensure_ascii=False))
        write_f.write('\n')
