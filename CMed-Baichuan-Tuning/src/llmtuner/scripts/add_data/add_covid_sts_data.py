import json
import random
import pandas as pd


ctc_file_path = '../../../../data/CHIP2023/sts/'
df_train = pd.read_csv(ctc_file_path + 'test.csv')
df_label = pd.read_csv(ctc_file_path + 'test.label.csv')
df_train['label'] = df_label['label']
print(df_train.head())

query1_list = df_train['query1'].tolist()
query2_list = df_train['query2'].tolist()
labels = df_train['label'].tolist()

# 加载temp
with open('../../../../data/CHIP2023/templates_augment.json', encoding='utf-8-sig') as f:
    temps = json.load(f)

temp_sts_list = temps['CHIP-STS']

chip_sts_flag = []
for idx in range(len(labels)):
    chip_sts_flag.append([query1_list[idx], query2_list[idx], labels[idx]])


sts_add_list = []
samp_chip_sts_flag = random.sample(chip_sts_flag, 2500)
for cme in samp_chip_sts_flag:
    if 1:
        samp_temp = random.choice(temp_sts_list)
        instruction_str = samp_temp
        instruction_str = instruction_str.replace('[INPUT_TEXT_1]', cme[0]).replace('[INPUT_TEXT_2]', cme[1]).replace('\\n', '\n')
        # samp_temp = samp_temp.replace('[INPUT_TEXT]', line['input']).replace('[LIST_LABELS]', '')

        target_str = ''
        if '是的，不是' in instruction_str:
            if cme[2] == 1:
                target_str = '是的'
            else:
                target_str = '不是'
        if '相同，不同' in instruction_str:
            if cme[2] == 1:
                target_str = '相同'
            else:
                target_str = '不同'

        print(instruction_str)
        print(target_str)
        print('----')

        new_dic = {}
        new_dic["instruction"] = instruction_str
        new_dic['input'] = ''
        new_dic['output'] = target_str
        sts_add_list.append(new_dic)

print(len(sts_add_list))

# with open("../../../../data/chip2023_train_cmeee_sts.json", "w") as f:
#     json.dump(chip_train_cmeee, f, ensure_ascii=False, indent=2)
#     print("加载入文件完成...")