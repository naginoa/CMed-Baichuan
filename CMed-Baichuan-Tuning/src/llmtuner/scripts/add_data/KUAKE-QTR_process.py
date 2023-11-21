import json
import sys

import random
input_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\KUAKE-QTR\KUAKE-QTR_train.json"
tarin_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\\train.json"
dev_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\dev.json"
test_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\Atest.json"
templates = "D:\load\pycharm\workplace\PromptCBLUE-main\src\data\\templates_augment.json"
output_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\process\process_KUAKE-QTR_junheng.json"
# task_dataset_dic=[]
# task_dataset_dic1 = []
list1=[]
list_train=[]
label_dic={"完全不匹配或者没有参考价值":0, "很少匹配有一些参考价值":0, "部分匹配":0, "完全匹配":0}

with open(tarin_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="KUAKE-QTR"):
            list_train.append(json_line["input"])
            target=json_line["target"]
            label_dic[target]+=1
print(label_dic)

#训练集 {'完全不匹配或者没有参考价值': 774, '很少匹配有一些参考价值': 1074, '部分匹配': 1161, '完全匹配': 1991}
# {'完全不匹配或者没有参考价值': 726, '很少匹配有一些参考价值': 426, '部分匹配': 339, '完全匹配': 1991}
label_dic={"完全不匹配或者没有参考价值":0, "很少匹配有一些参考价值":0, "部分匹配":0, "完全匹配":0}
with open(dev_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="KUAKE-QTR"):
            list_train.append(json_line["input"])
            target = json_line["target"]
            label_dic[target] += 1
print(label_dic)
#验证集 {'完全不匹配或者没有参考价值': 62, '很少匹配有一些参考价值': 105, '部分匹配': 85, '完全匹配': 148}
# exit()
with open(test_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="KUAKE-QTR"):
            list_train.append(json_line["input"])
with open(templates, 'r', encoding='utf-8') as f:
    templates= json.load(f)
    templates["KUAKE-QTR"]

output_template="具有[RELATION]关系的头尾实体对如下："
output_content="头实体为[SUBJECT]，尾实体为[OBJECT]。"
label_list=["完全不匹配或者没有参考价值", "很少匹配有一些参考价值", "部分匹配", "完全匹配"]
with open(input_dir, 'r', encoding='utf-8') as f:
    line_list=json.load(f)
    for json_line in line_list:
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        query=json_line["query"]
        text=query
        flag = 0
        for i in range(len(list_train)):
            if text in list_train[i]:
                print(text+"\n")
                flag=1
        if flag==0:
            title=json_line["title"]
            label = json_line["label"]

            slice = random.randint(0,len(templates["KUAKE-QTR"])-1)
            input_=templates["KUAKE-QTR"][slice]
            input_=input_.replace("[INPUT_TEXT_1]",query)
            input_ = input_.replace("[INPUT_TEXT_2]", title)
            input_ = input_.replace("[LIST_LABELS]", "完全不匹配或者没有参考价值，很少匹配有一些参考价值，部分匹配，完全匹配")

            output=label_list[int(label)]
            # print(output)
            # exit()
            txt_json={}
            txt_json["input"]=input_
            txt_json["target"]=output
            txt_json["answer_choices"] = ["完全不匹配或者没有参考价值", "很少匹配有一些参考价值", "部分匹配", "完全匹配"]
            txt_json["task_type"] = "nli"
            txt_json["task_dataset"] = "KUAKE-QTR"
            txt_json["sample_id"] = "0"
            list1.append(txt_json)
            # if(len(list1)==1000):
            #     break
        # print("\n具有化疗关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为化疗。头实体为脉络丛乳头状癌，尾实体为术前化疗。\n具有预后生存率关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为5年生存率75%。头实体为脉络丛乳头状癌，尾实体为10年生存率66. 6%。\n具有手术治疗关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为手术全切。")
        # print(input_)
        # task_dataset=json_line["task_dataset"]
        # task_dataset_dic.append(task_dataset)
random.shuffle(list1)
print(len(list1))
list2=[]
label_dic={"完全不匹配或者没有参考价值":0, "很少匹配有一些参考价值":0, "部分匹配":0, "完全匹配":0}
for item in list1:
    target=item["target"]
    if label_dic[target]<250:
        list2.append(item)
        label_dic[target]+=1

with open(output_dir, 'w', encoding='utf-8') as write_f:
    count=0
    for i in range(1000):
        write_f.write(json.dumps(list2[i], ensure_ascii=False))
        write_f.write('\n')
