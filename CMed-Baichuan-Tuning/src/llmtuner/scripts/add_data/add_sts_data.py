import json
import random


sts_file_path = '../../../../data/CHIP2023/sts/CHIP-STS_train.json'
# 读取训练集
with open(sts_file_path, encoding='utf-8-sig') as f:
    chip_sts = json.load(f)

# query1_list为chip_sts数组中的每个元素的text1字段
query1_list = [chip_sts[i]['text1'] for i in range(len(chip_sts))]
# query2_list为chip_sts数组中的每个元素的text2字段
query2_list = [chip_sts[i]['text2'] for i in range(len(chip_sts))]
# labels为chip_sts数组中的每个元素的label字段
labels = [chip_sts[i]['label'] for i in range(len(chip_sts))]

# 加载temp
with open('../../../../data/CHIP2023/templates_augment.json', encoding='utf-8-sig') as f:
    temps = json.load(f)

temp_sts_list = temps['CHIP-STS']

chip_sts_flag = []
for idx in range(len(labels)):
    chip_sts_flag.append([query1_list[idx], query2_list[idx], labels[idx]])

sts_add_list = []
samp_chip_sts_flag = random.sample(chip_sts_flag, 1000)

for cme in samp_chip_sts_flag:
    if 1:
        samp_temp = random.choice(temp_sts_list)
        instruction_str = samp_temp
        instruction_str = instruction_str.replace('[INPUT_TEXT_1]', cme[0]).replace('[INPUT_TEXT_2]', cme[1]).replace('\\n', '\n')
        # samp_temp = samp_temp.replace('[INPUT_TEXT]', line['input']).replace('[LIST_LABELS]', '')

        target_str = ''
        if '是的，不是' in instruction_str:
            if cme[2] == '1':
                target_str = '是的'
            else:
                target_str = '不是'
        if '相同，不同' in instruction_str:
            if cme[2] == '1':
                target_str = '相同'
            else:
                target_str = '不同'

        print(instruction_str)
        print(target_str)
        print('----')

        new_dic = {}
        new_dic['input'] = instruction_str
        new_dic["target"] = target_str
        new_dic['task_dataset'] = 'CHIP-STS'
        sts_add_list.append(new_dic)

print(len(sts_add_list))

# 存储。jsonlines格式
with open("../../../../data/CHIP2023/new_add/CHIP-STS_aug.json", "w") as f:
    for line in sts_add_list:
        json.dump(line, f, ensure_ascii=False)
        f.write('\n')


# with open("../../../../data/chip2023_train_cmeee_sts.json", "w") as f:
#     json.dump(chip_train_cmeee, f, ensure_ascii=False, indent=2)
#     print("加载入文件完成...")