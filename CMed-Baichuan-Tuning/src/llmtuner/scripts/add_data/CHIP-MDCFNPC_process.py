import json
import sys

import random
input_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\CHIP-MDCFNPC\CHIP-MDCFNPC_train.jsonl"
tarin_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\\train.json"
dev_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\dev.json"
test_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\Atest.json"
templates = "D:\load\pycharm\workplace\PromptCBLUE-main\src\data\\templates_augment.json"
output_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\process\process_CHIP-MDCFNPC-chongfu1.json"
# task_dataset_dic=[]
# task_dataset_dic1 = []
list1=[]
list_train=[]


with open(tarin_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="CHIP-MDCFNPC"):
            list_train.append(json_line["input"])
with open(dev_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="CHIP-MDCFNPC"):
            list_train.append(json_line["input"])
with open(test_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="CHIP-MDCFNPC"):
            list_train.append(json_line["input"])
with open(templates, 'r', encoding='utf-8') as f:
    templates= json.load(f)
    templates["CHIP-MDCFNPC"]

output_template="上述对话中临床发现实体以及其阴阳性判别如下：\n"


with open(input_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        dialog_info=json_line["dialog_info"]
        text0=dialog_info[0]["text"]
        flag = 0
        for i in range(len(list_train)):
            if text0 in list_train[i]:
                # print(text0+"\n")
                flag=1
                break
        if flag==0:
            COUNT=random.randint(1,4)
            for c in range(COUNT):
                ner_dic={}
                text_line=""
                ran=random.randint(1,len(dialog_info))
                for line in dialog_info[:ran:]:
                    text=line["text"]
                    ner=line["ner"]
                    sender=line["sender"]
                    text_line+=sender+"："+text+"\n"
                    # print(text_line)
                    for ner_item in ner:
                        mention=ner_item["mention"]
                        type=ner_item["type"]
                        attr=ner_item["attr"]
                        if mention not in ner_dic:
                            ner_dic[mention]=attr
                text_line=text_line[:-1:]
                # print(ner_dic)

                slice = random.randint(0,len(templates["CHIP-MDCFNPC"])-1)
                input_=templates["CHIP-MDCFNPC"][slice]
                input_=input_.replace("[INPUT_TEXT]",text_line)

                input_ = input_.replace("[LIST_LABELS]", "阳性，阴性，其他，不标注")
                input_ = input_.replace("[LIST_MENTIONS]", '，'.join(ner_dic.keys()))
                # print(input_)
                # exit()
                output=output_template
                for k,y in ner_dic.items():
                    output+=k+"："+y+"\n"
                output=output[:-1:]

                txt_json={}
                txt_json["input"]=input_
                txt_json["target"]=output
                txt_json["answer_choices"] = ["阳性", "阴性", "其他", "不标注"]
                txt_json["task_type"] = "attr_cls"
                txt_json["task_dataset"] = "CHIP-MDCFNPC"
                txt_json["sample_id"] = "0"
                list1.append(txt_json)
                # print(txt_json)
                # exit()
                # print(list1)
                # print(COUNT)
                if(len(list1)==1000):
                    break

            # print("\n具有化疗关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为化疗。头实体为脉络丛乳头状癌，尾实体为术前化疗。\n具有预后生存率关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为5年生存率75%。头实体为脉络丛乳头状癌，尾实体为10年生存率66. 6%。\n具有手术治疗关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为手术全切。")
            # print(input_)
            # task_dataset=json_line["task_dataset"]
            # task_dataset_dic.append(task_dataset)
list1=list1[:2000:]
random.shuffle(list1)
print(len(list1))
with open(output_dir, 'w', encoding='utf-8') as write_f:
    count=0
    for i in range(1000):
        write_f.write(json.dumps(list1[i], ensure_ascii=False))
        write_f.write('\n')
