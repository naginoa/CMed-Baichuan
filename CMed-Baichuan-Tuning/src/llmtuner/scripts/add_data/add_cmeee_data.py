import json
import random


label_dic = {
    'dis': '疾病',
    'sym': '临床表现',
    'pro': '医疗程序',
    'equ': '医疗设备',
    'dru': '药物',
    'ite': '医学检验项目',
    'bod': '身体部位',
    'dep': '医院科室',
    'mic': '微生物类'
}


chip_merge_datafile = '../../../../data/chip2023_merge.json'
chip_test_datafile = '../../../../data/chip2023_test.json'
cmeee_train_datafile = '../../../../data/CHIP2023/cmeee/CMeEE-V2_train.json'

with open(chip_merge_datafile, encoding='utf-8-sig') as f:
    chip_merge = json.load(f)

with open(chip_test_datafile, encoding='utf-8-sig') as f:
    chip_test = json.load(f)

with open(cmeee_train_datafile, encoding='utf-8-sig') as f:
    chip_cmeee = json.load(f)

# 给cmeee中在数据集出现的数据打上flag
# flag = 0
# for cme in chip_cmeee:
#     for each_cm in chip_merge:
#         if cme['text'] in each_cm['instruction']:
#             cme['flag'] = 1
#             flag += 1
#
# for cme in chip_cmeee:
#     for each_cm in chip_test:
#         if cme['text'] in each_cm['instruction']:
#             cme['flag'] = 1
#             flag += 1
#
# with open("../../../data/CHIP2023/cmeee/CMeEE-V2_train_flag.json", "w") as f:
#     json.dump(chip_cmeee, f, ensure_ascii=False, indent=2)
#     print("加载入文件完成...")

with open("../../../../data/CHIP2023/cmeee/CMeEE-V2_train_flag.json", encoding='utf-8-sig') as f:
    chip_cmeee_flag = json.load(f)

# 加载temp
with open('../../../../data/CHIP2023/templates_augment.json', encoding='utf-8-sig') as f:
    temps = json.load(f)

target_prompt = '上述句子中的实体包含：'
temp_cmeee_list = temps['CMeEE-V2']

cmeee_add_list = []
# samp_chip_cmeee_flag 为flag不为1的数据
samp_chip_cmeee_flag = []
for cme in chip_cmeee_flag:
    if cme.get('flag') != 1:
        samp_chip_cmeee_flag.append(cme)

samp_chip_cmeee_flag = random.sample(samp_chip_cmeee_flag, 1000)
for cme in samp_chip_cmeee_flag:
    if cme.get('flag') != 1:
        choices_ents = label_dic.values()
        ents_key = [label_dic.get(i["type"]) for i in cme["entities"]]
        ents_value = [i["entity"] for i in cme["entities"]]

        samp_temp = random.choice(temps['CMeEE-V2'])
        instruction_str = samp_temp
        instruction_str = instruction_str.replace('[INPUT_TEXT]', cme['text']).replace('[LIST_LABELS]', '，'.join(choices_ents)).replace('\\n', '\n')
        # samp_temp = samp_temp.replace('[INPUT_TEXT]', line['input']).replace('[LIST_LABELS]', '')

        target_str = target_prompt
        for key, value in zip(ents_key, ents_value):
            target_str += '\n{}实体：{}'.format(key, value)

        print(instruction_str)
        print(target_str)
        print('----')

        instruction_str = instruction_str.replace('\n答：', '')

        # 生成新的数据
        new_dic = {}
        new_dic['input'] = instruction_str
        new_dic["target"] = target_str
        new_dic["task_dataset"] = "CMeEE-V2"
        cmeee_add_list.append(new_dic)

# 读取原训练集
# with open('../../../../../data/chip2023.json', encoding='utf-8-sig') as f:
# #     chip_train = json.load(f)
# #
# # print(random.sample(chip_train, 5))
# # print(random.sample(cmeee_add_list, 5))
# #
# # chip_train.extend(cmeee_add_list)
# ../../../../data/CHIP2023/new_add/

# 保存新的数据,将数据存为jsonline格式，而不是json格式
with open("../../../../data/CHIP2023/new_add/CMeEE-V2_aug.json", "w") as f:
    for each in cmeee_add_list:
        json.dump(each, f, ensure_ascii=False)
        f.write('\n')
    print("加载入文件完成...")
