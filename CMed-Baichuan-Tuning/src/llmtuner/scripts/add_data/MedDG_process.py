import json
import sys

import random
input_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\MedDG\MedDG_train.json"
tarin_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\\train.json"
dev_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\dev.json"
test_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\Atest.json"
templates = "D:\load\pycharm\workplace\PromptCBLUE-main\src\data\\templates_augment.json"
output_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\process\process_MedDG.json"
# task_dataset_dic=[]
# task_dataset_dic1 = []
list1=[]
list_train=[]


with open(tarin_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="MedDG"):
            list_train.append(json_line["input"])
with open(dev_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="MedDG"):
            list_train.append(json_line["input"])
with open(test_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="MedDG"):
            list_train.append(json_line["input"])
with open(templates, 'r', encoding='utf-8') as f:
    templates= json.load(f)
    templates["MedDG"]

output_template="具有[RELATION]关系的头尾实体对如下："
output_content="头实体为[SUBJECT]，尾实体为[OBJECT]。"

with open(input_dir, 'r', encoding='utf-8') as f:
    lines_list=json.load(f)
    for lines in lines_list:
        text_lines=""

        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        flag = 0
        text0=lines[0]["Sentence"]
        for i in range(len(list_train)):
            if text0 in list_train[i]:
                # print(text0+"\n")
                flag=1
        if flag==0:
            print(text0 + "\n")
            ren=random.randint(5,len(lines)-1)
            print(ren)
            count=0
            while lines[ren-1]["id"]=="Doctor" or lines[ren]["id"]=="Patient":
                ren = random.randint(len(lines)//2, len(lines)-1)
                count+=1
                if count==5:
                    break
                # print(len(lines)-1,ren)

            for i in range(ren):
                json_line=lines[i]
                id = json_line["id"]
                te = json_line["Sentence"]
                if i!=0 and lines[i-1]["id"]!=id:
                    text_lines+="\n"
                if id=="Patient":
                    id="患者："
                else:
                    id="医生："
                text_lines+=id+te+"\n"
            text_lines=text_lines[:-1:]

            slice = random.randint(0,len(templates["MedDG"])-1)
            input_=templates["MedDG"][slice]
            input_=input_.replace("[INPUT_TEXT]",text_lines)

            # print(input_)
            # exit()
            if(lines[ren]["id"]=="Doctor"):
                output=lines[ren]["Sentence"]
                txt_json = {}
                txt_json["input"] = input_
                txt_json["target"] = output
                txt_json["answer_choices"] = None
                txt_json["task_type"] = "response_generation"
                txt_json["task_dataset"] = "MedDG"
                txt_json["sample_id"] = "0"
                list1.append(txt_json)
                print(len(list1))
            else:
                print("出错")

            # print(list1)

            if(len(list1)==10000):
                break
        # print("\n具有化疗关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为化疗。头实体为脉络丛乳头状癌，尾实体为术前化疗。\n具有预后生存率关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为5年生存率75%。头实体为脉络丛乳头状癌，尾实体为10年生存率66. 6%。\n具有手术治疗关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为手术全切。")
        # print(input_)
        # task_dataset=json_line["task_dataset"]
        # task_dataset_dic.append(task_dataset)
random.shuffle(list1)
with open(output_dir, 'w', encoding='utf-8') as write_f:
    count=0
    for i in range(1000):
        write_f.write(json.dumps(list1[i], ensure_ascii=False))
        write_f.write('\n')
