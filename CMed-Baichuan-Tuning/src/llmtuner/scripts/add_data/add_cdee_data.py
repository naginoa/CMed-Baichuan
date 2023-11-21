import json
import random


chip_merge_datafile = '../../../../data/chip2023_merge.json'
chip_test_datafile = '../../../../data/chip2023_test.json'
cdee_train_datafile = '../../../../data/CHIP2023/cdee/CHIP-CDEE_train.json'
cdee_dev_datafile = '../../../../data/CHIP2023/cdee/CHIP-CDEE_dev.json'

with open(chip_merge_datafile, encoding='utf-8-sig') as f:
    chip_merge = json.load(f)

with open(chip_test_datafile, encoding='utf-8-sig') as f:
    chip_test = json.load(f)

with open(cdee_train_datafile, encoding='utf-8-sig') as f:
    chip_cdee = json.load(f)

with open(cdee_dev_datafile, encoding='utf-8-sig') as f:
    chip_cdee_dev = json.load(f)

chip_cdee.extend(chip_cdee_dev)

# 统计chip_cdee中'text'值未在chip_merge和chip_test中出现的次数
flag = 0
chip_merge_str = str(chip_merge)
for cdee in chip_cdee:
    if cdee['text'] in chip_merge_str:
        cdee['flag'] = 1
        flag += 1

chip_test_str = str(chip_test)
for cdee in chip_cdee:
    if cdee['text'] in chip_test_str:
        cdee['flag'] = 1
        flag += 1

print(flag)
print(len(chip_cdee))

# chip_cdee只保留'text'值未在chip_merge和chip_test中出现的数据
chip_cdee_add = []
for cdee in chip_cdee:
    if 'flag' not in cdee:
        chip_cdee_add.append(cdee)

# 目前chip_cdee_add中有364条数据，随机抽取236条数据
chip_cdee_add_sample = random.sample(chip_cdee_add, 236)
chip_cdee_add.extend(chip_cdee_add_sample)

# 加载temp
with open('../../../../data/CHIP2023/templates_augment.json', encoding='utf-8-sig') as f:
    temps = json.load(f)

target_prompt = '上述句子中的临床发现事件如下：'

res_lines = []
random.shuffle(chip_cdee_add)

for cme in chip_cdee_add:
    samp_temp = random.choice(temps['CHIP-CDEE'])
    instruction_str = samp_temp
    instruction_str = instruction_str.replace('[INPUT_TEXT]', cme['text']).replace('\\n', '\n')
    print(instruction_str)

    target_str = target_prompt
    events = cme['event']
    for event in events:
        target_str += '\n主体词：' + event['core_name'] + '；' if event['core_name'] != '' else ''
        target_str += '发生状态：' + event['tendency'] + '；' if event['tendency'] != '' else ''
        target_str += '描述词：'
        target_str += '，'.join(event["character"]) + '；' if event["character"] != [] else ''
        target_str += '解剖部位：'
        target_str += '，'.join(event["anatomy_list"]) if event["anatomy_list"] != [] else ''
    print(target_str)

    instruction_str = instruction_str.replace('\n答：', '')

    # 生成新的数据
    new_dic = {}
    new_dic["input"] = instruction_str
    new_dic["target"] = target_str
    new_dic["task_dataset"] = "CHIP-CDEE"
    res_lines.append(new_dic)

# 保存新的数据,将数据存为jsonline格式，而不是json格式
with open('../../../../data/CHIP2023/new_add/CHIP-CDEE_aug.json', 'w', encoding='utf-8') as f:
    for line in res_lines:
        json.dump(line, f, ensure_ascii=False)
        f.write('\n')
