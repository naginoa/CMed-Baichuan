import json
import random


qqr_train_datafile = '../../../../data/CHIP2023/qqr/KUAKE-QQR_train.json'
qqr_dev_datafile = '../../../../data/CHIP2023/qqr/KUAKE-QQR_dev.json'

# 读取qqr_train_datafile, 用json.load()方法
with open(qqr_train_datafile, encoding='utf-8-sig') as f:
    chip_qqr = json.load(f)

# 读取qqr_dev_datafile, 用json.load()方法
# with open(qqr_dev_datafile, encoding='utf-8-sig') as f:
#     chip_qqr_dev = json.load(f)

# chip_qqr.extend(chip_qqr_dev)

# 加载temp
with open('../../../../data/CHIP2023/templates_augment.json', encoding='utf-8-sig') as f:
    temps = json.load(f)

print(len(chip_qqr))

chip_merge_datafile = '../../../../data/CHIP2023/chip/merge.json'
chip_test_datafile = '../../../../data/CHIP2023/A_test.json'

# 用读取jsonlines的方式读取chip_merge_datafile
with open(chip_merge_datafile, 'r', encoding='utf-8-sig') as f:
    chip_merge = f.readlines()

# 用读取jsonlines的方式读取chip_test_datafile
with open(chip_test_datafile, 'r', encoding='utf-8-sig') as f:
    chip_test = f.readlines()

# chip_merge和chip_test合并
chip_merge.extend(chip_test)
print(len(chip_merge))

# chip_merge_qqr为chip_merge中的元素"task_dataset"为"KUAKE-QQR"的元素
chip_merge_qqr = []
for merge in chip_merge:
    merge = json.loads(merge)
    if merge['task_dataset'] == 'KUAKE-QQR':
        chip_merge_qqr.append(merge)

# 判断chip_qqr中的元素'query1'和'query2'是否同时存在chip_merge_qqr的某一行中，若存在则打flag为1并break
for qqr in chip_qqr:
    for merge in chip_merge_qqr:
        if qqr['query1'] in merge['input'] and qqr['query2'] in merge['input']:
            qqr['flag'] = 1
            break

# 统计chip_qqr中flag为1的元素有多少
count = 0
for qqr in chip_qqr:
    if qqr.get('flag') == 1:
        count += 1

print('---', count)

# chip_qqr_flag0为chip_qqr中flag不为1的元素
chip_qqr_flag0 = []
for qqr in chip_qqr:
    if qqr.get('flag') != 1:
        chip_qqr_flag0.append(qqr)

# 统计chip_qqr_flag0中每个元素的'label'值有几种
label_count = {}
for qqr in chip_qqr_flag0:
    label = qqr.get('label')
    if label not in label_count:
        label_count[label] = 1
    else:
        label_count[label] += 1

print(label_count)

# chip_qqr_label2为chip_qqr_flag0中'label'值为2的元素
chip_qqr_label2 = []
for qqr in chip_qqr_flag0:
    if qqr.get('label') == '2':
        chip_qqr_label2.append(qqr)

print(len(chip_qqr_label2))

# chip_qqr_label2_sample为chip_qqr_label2中随机抽取的1000个元素
chip_qqr_label2_sample = random.sample(chip_qqr_label2, 600)

# chip_qqr_label1为chip_qqr_flag0中'label'值为1的元素
chip_qqr_label1 = []
for qqr in chip_qqr_flag0:
    if qqr.get('label') == '1':
        chip_qqr_label1.append(qqr)

print(len(chip_qqr_label1))
print(chip_qqr_label1[:5])

# 将chip_qqr_label1的元素的query1和query2互换
for qqr in chip_qqr_label1:
    qqr['query1'], qqr['query2'] = qqr['query2'], qqr['query1']

chip_qqr_label1_sample = random.sample(chip_qqr_label1, 600)

qqr_add_list = []

for qqr in chip_qqr_label2_sample:
    samp_temp = random.choice(temps['KUAKE-QQR'])

    labels_choices = ["完全一致", "后者是前者的语义子集", "后者是前者的语义父集", "语义无直接关联"]

    instruction_str = samp_temp
    instruction_str = instruction_str.replace('[INPUT_TEXT_1]', qqr['query1']).replace('[INPUT_TEXT_2]', qqr['query2'])\
        .replace('[LIST_LABELS]', '，'.join(labels_choices)).replace('\\n', '\n')

    target = "完全一致"
    instruction_str = instruction_str.replace('\n答：', '').replace(' 答：', '')

    new_dic = {
        "input": instruction_str,
        "target": target,
        "task_dataset": "KUAKE-QQR",
    }
    qqr_add_list.append(new_dic)

print(len(qqr_add_list))
print(qqr_add_list[:5])

for qqr in chip_qqr_label1_sample:
    samp_temp = random.choice(temps['KUAKE-QQR'])

    labels_choices = ["完全一致", "后者是前者的语义子集", "后者是前者的语义父集", "语义无直接关联"]

    instruction_str = samp_temp
    instruction_str = instruction_str.replace('[INPUT_TEXT_1]', qqr['query1']).replace('[INPUT_TEXT_2]', qqr['query2'])\
        .replace('[LIST_LABELS]', '，'.join(labels_choices)).replace('\\n', '\n')

    target = "后者是前者的语义父集"
    instruction_str = instruction_str.replace('\n答：', '').replace(' 答：', '')

    new_dic = {
        "input": instruction_str,
        "target": target,
        "task_dataset": "KUAKE-QQR",
    }
    qqr_add_list.append(new_dic)

print(len(qqr_add_list))
print(qqr_add_list[600:605])

# 存jsonlines
with open('../../../../data/CHIP2023/new_add/KUAKE-QQR_aug.json', 'w', encoding='utf-8-sig') as f:
    for dic in qqr_add_list:
        json.dump(dic, f, ensure_ascii=False)
        f.write('\n')
