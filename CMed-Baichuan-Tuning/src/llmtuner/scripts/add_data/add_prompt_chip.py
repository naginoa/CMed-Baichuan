import random
import json


filepath = '../../../../data/CHIP2023/'
null = ''

res_lines = []

with open(filepath + '/chip/train.json', encoding='utf-8') as f1:
    for line in f1.readlines():
        line = eval(line)

        prompt_line = '进行{}任务，任务类型为{}\n'
        # print(line["input"])
        # print(line['task_type'])
        # print(line['task_dataset'])
        # print(prompt_line.format(line['task_dataset'], line['task_type'])+line["input"])
        line['input'] = prompt_line.format(line['task_dataset'], line['task_type'])+line["input"]

        new_dic = {}
        new_dic["instruction"] = line['input']
        new_dic['input'] = ''
        new_dic['output'] = line['target']

        # print(new_dic)
        res_lines.append(new_dic)


with open("../../../../data/chip2023_train_prompt1.json", "w") as f:
    json.dump(res_lines, f, ensure_ascii=False, indent=2)
    print("加载入文件完成...")

res_lines = []

with open(filepath + 'A_test.json', encoding='utf-8') as f1:
    for line in f1.readlines():
        line = eval(line)

        prompt_line = '进行{}任务，任务类型为{}\n'
        line['input'] = prompt_line.format(line['task_dataset'], line['task_type']) + line["input"]

        new_dic = {}
        new_dic["instruction"] = line['input']
        new_dic['input'] = ''
        new_dic['output'] = line['target']

        res_lines.append(new_dic)

with open("../../../../data/chip2023_test_prompt1.json", "w") as f:
    json.dump(res_lines, f, ensure_ascii=False, indent=2)
    print("加载入文件完成...")
