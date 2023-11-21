import json
import sys

import random
input_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\CMeIE-V2\CMeIE-V2_train.jsonl"
tarin_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\\train.json"
dev_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\dev.json"
test_dir="D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\chip_original_data\Atest.json"
templates = "D:\load\pycharm\workplace\PromptCBLUE-main\src\data\\templates_augment.json"
output_dir = "D:\load\pycharm\workplace\PromptCBLUE-main\datasets\PromptCBLUE\process\process_CMeIE-V2.json"
# task_dataset_dic=[]
# task_dataset_dic1 = []
list1=[]
list_train=[]
list_labels=['预后生存率', '化疗', '手术治疗', '病理分型', '病因', '同义词', '发病机制', '发病率', '发病性别倾向', '相关（导致）',
             '药物治疗', '临床表现', '辅助治疗', '并发症', '鉴别诊断', '多发群体', '辅助检查', '相关（症状）', '影像学检查',
             '实验室检查', '阶段', '病理生理', '内窥镜检查', '预防', '筛查', '高危因素', '放射治疗', '发病部位', '遗传因素',
             '病史', '多发地区', '发病年龄', '外侵部位', '相关（转化）', '预后状况', '组织学检查', '侵及周围组织转移的症状',
             '治疗后症', '就诊科室', '转移部位', '死亡率', '风险评估因素', '传播途径', '多发季节']

with open(tarin_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="CMeIE-V2"):
            list_train.append(json_line["input"])
with open(dev_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="CMeIE-V2"):
            list_train.append(json_line["input"])
with open(test_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        if(json_line["task_dataset"]=="CMeIE-V2"):
            list_train.append(json_line["input"])
with open(templates, 'r', encoding='utf-8') as f:
    templates= json.load(f)
    templates["CMeIE-V2"]

output_template="具有[RELATION]关系的头尾实体对如下："
output_content="头实体为[SUBJECT]，尾实体为[OBJECT]。"

with open(input_dir, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # loads()：用于处理内存中的json对象，strip去除可能存在的空格
        json_line = json.loads(line.strip())
        text=json_line["text"]
        flag = 0
        for i in range(len(list_train)):
            if text in list_train[i]:
                print(text+"\n")
                flag=1
        if flag==0:
            spo_list=json_line["spo_list"]
            relations_dic = {}
            for i in range(len(spo_list)):
                predicate=spo_list[i]["predicate"]#关系
                subject=spo_list[i]["subject"]#头实体
                object=spo_list[i]["object"]
                object_value=object["@value"]#尾实体
                if predicate not in relations_dic:
                    relations_dic[predicate]=[]
                tmp_list=relations_dic[predicate]
                head_tail=[0,1]
                head_tail[0]=subject
                head_tail[1]=object_value
                tmp_list.append(head_tail)
                relations_dic[predicate]=tmp_list

            slice = random.randint(0,len(templates["CMeIE-V2"])-1)
            input_=templates["CMeIE-V2"][slice]
            input_=input_.replace("[INPUT_TEXT]",text)
            ren=random.randint(25,30)
            labels_list=random.sample(list_labels, ren)
            for k in relations_dic.keys():
                if k not in labels_list:
                    ran=random.randint(0,len(labels_list)-1)
                    labels_list.insert(ran,k)
            labels="，".join(labels_list)
            input_ = input_.replace("[LIST_LABELS]", labels)
            # print(input_)
            # exit()
            output=""

            count_relation=0
            for k,y in relations_dic.items():
                if(count_relation!=0):
                    output+="\n"
                output_template1=output_template.replace("[RELATION]",k)
                output+=output_template1
                for i in range(len(y)):
                    output_content1=output_content.replace("[SUBJECT]",y[i][0])
                    output_content2=output_content1.replace("[OBJECT]", y[i][1])
                    output+=output_content2
                count_relation+=1
            # print(input_)

            txt_json={}
            txt_json["input"]=input_
            txt_json["target"]=output
            txt_json["answer_choices"] = labels_list
            txt_json["task_type"] = "spo_generation"
            txt_json["task_dataset"] = "CMeIE-V2"
            txt_json["sample_id"] = "0"
            list1.append(txt_json)
            if(len(list1)==1000):
                break
        # print("\n具有化疗关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为化疗。头实体为脉络丛乳头状癌，尾实体为术前化疗。\n具有预后生存率关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为5年生存率75%。头实体为脉络丛乳头状癌，尾实体为10年生存率66. 6%。\n具有手术治疗关系的头尾实体对如下：头实体为脉络丛乳头状癌，尾实体为手术全切。")
        # print(input_)
        # task_dataset=json_line["task_dataset"]
        # task_dataset_dic.append(task_dataset)

with open(output_dir, 'w', encoding='utf-8') as write_f:
    count=0
    for i in range(len(list1)):
        write_f.write(json.dumps(list1[i], ensure_ascii=False))
        write_f.write('\n')
