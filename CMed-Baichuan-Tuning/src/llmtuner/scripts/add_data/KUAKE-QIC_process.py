import json
import sys

import random
input_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\KUAKE-QIC\KUAKE-QIC_train.json"
tarin_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\\train.json"
dev_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\dev.json"
test_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\Atest.json"
templates = "D:\load\pycharm\workplace\PromptCBLUE-main\src\data\\templates_augment.json"
output_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\process\process_KUAKE-QIC_junheng.json"
# task_dataset_dic=[]
# task_dataset_dic1 = []
list1=[]
list_train=[]
list_labels=['治疗方案','疾病表述','非上述类型', '病因分析', '注意事项', '功效作用', '病情诊断', '就医建议', '医疗费用', '指标解读', '后果表述']
ans_dic={}
with open(tarin_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="KUAKE-QIC"):
            list_train.append(json_line["input"])
            target=json_line["target"]
            if target not in list_labels:
                list_labels.append(target)

# print(list_labels)
# exit()
with open(dev_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="KUAKE-QIC"):
            list_train.append(json_line["input"])
with open(test_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="KUAKE-QIC"):
            list_train.append(json_line["input"])
with open(templates, 'r', encoding='utf-8') as f:
    templates= json.load(f)
    templates["KUAKE-QIC"]

output_template="具有[RELATION]关系的头尾实体对如下："
output_content="头实体为[SUBJECT]，尾实体为[OBJECT]。"
label_dic={'就医建议': 500, '治疗方案': 500, '疾病表述': 500, '医疗费用': 500, '非上述类型': 500, '病情诊断': 500, '注意事项': 500, '功效作用': 500, '病因分析': 500, '指标解读': 500, '后果表述': 500}


with open(input_dir, 'r', encoding='utf-8') as f:
    line_list=json.load(f)
    for json_line in line_list:
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        text=json_line["query"]
        label=json_line["label"]
        flag = 0
        for i in range(len(list_train)):
            if text in list_train[i]:
                # print(text+"\n")
                flag=1
        if flag==0:
            # if label not in label_dic:
            #     label_dic[label]=1
            # else:
            #     label_dic[label] += 1
            r1 = random.randint(1, 2)
            #          10                 6                 4            27
            if label=="医疗费用" or label=="病因分析" or label=="指标解读" :
                r1 = random.randint(3, 8)
            if label == "后果表述":
                r1 = random.randint(3, 6)
            for r2 in range(r1):
                slice = random.randint(0,len(templates["KUAKE-QIC"])-1)
                input_=templates["KUAKE-QIC"][slice]
                input_=input_.replace("[INPUT_TEXT]",text)
                ren=random.randint(8,11)
                labels_list=random.sample(list_labels, ren)
                if label=="其他":
                    label="非上述类型"
                if label not in labels_list:
                    ran=random.randint(0,len(labels_list)-1)
                    labels_list.insert(ran,label)
                labels="，".join(labels_list)

                input_ = input_.replace("[LIST_LABELS]", labels)
                # print(input_)
                # exit()
                output=label
                txt_json={}
                txt_json["input"]=input_
                txt_json["target"]=output
                txt_json["answer_choices"] = labels_list
                txt_json["task_type"] = "cls"
                txt_json["task_dataset"] = "KUAKE-QIC"
                txt_json["sample_id"] = "0"
                list1.append(txt_json)


            # if(len(list1)==1100):
            #     break
print(len(list1))
random.shuffle(list1)
list2=[]
print(label_dic)
label_dic={'就医建议': 0, '治疗方案': 0, '疾病表述': 0, '医疗费用': 0, '非上述类型': 0, '病情诊断': 0, '注意事项': 0, '功效作用': 0, '病因分析': 0, '指标解读': 0, '后果表述': 0}
for item in list1:
    target=item["target"]
    if label_dic[target] < 128:
        list2.append(item)
        label_dic[target]+=1
print(len(list2))
print(label_dic)



with open(output_dir, 'w', encoding='utf-8') as write_f:
    count=0
    for i in range(1100):
        write_f.write(json.dumps(list2[i], ensure_ascii=False))
        write_f.write('\n')
