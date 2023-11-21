import json


ori_dev_path = '../../../data/CHIP2023/chip/dev.json'
ckp_path = 'chip2023-lr2e4-bs4-grad4/pred-ckp25500-dev'
ckp_dev_path = '../../../../data/chip2023/{}/dev_predictions.json'.format(ckp_path)
# ../../../../data/chip2023/chip2023-lr2e4-bs4-grad4/pred-ckp25500-dev/
print(ckp_dev_path)

null = ''
rm_lines = []

ori_lines = []
with open(ori_dev_path, encoding='utf-8-sig') as f:
    for line in f.readlines():
        line = eval(line)
        # line = json.loads(line)
        # line = json.dumps(line, ensure_ascii=False)
        ori_lines.append(line)

ckp_lines = []
with open(ckp_dev_path, encoding='utf-8-sig') as f:
    for line in f.readlines():
        line = eval(line)
        ckp_lines.append(line)

print(len(ori_lines))
print(len(ckp_lines))

complete_equal_flag = 0
for ori, ckp in zip(ori_lines, ckp_lines):
    if ori['target'] == ckp['target']:
        complete_equal_flag += 1
    else:
        tmp_dic = {}
        tmp_dic['instruction'] = ori['input']
        tmp_dic['input'] = ''
        tmp_dic['output'] = [ori['target'], ckp['target']]
        rm_lines.append(tmp_dic)

print(complete_equal_flag / len(ori_lines))
for i in rm_lines[:5]:
    print(i)

with open("../../../data/chip2023_rm_dev.json", "w") as f:
    json.dump(rm_lines, f, ensure_ascii=False, indent=2)
    print("加载入文件完成...")

