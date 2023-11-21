import json
import random

# ['体征(医生检测）', '治疗或手术', '成瘾行为', '伦理审查', '性别', '过敏耐受', '含有多个类别', '疾病', '饮食', '预期寿命', '种族', '肿瘤进展', '疾病分期', '风险评估', '年龄', '症状(患者感受)', '药物', '性取向', '读写能力', '献血', '研究者决定', '能力', '酒精使用', '器官组织状态', '口腔相关', '健康群体', '病例来源', '参与其它试验', '残疾群体', '实验室检查', '教育情况', '依存性', '居住情况', '怀孕相关', '诊断', '睡眠', '锻炼', '受体状态', '设备', '数据可及性', '吸烟状况', '特殊病人特征', '知情同意', '护理']
# ['Therapy or Surgery', 'Sign', 'Addictive Behavior', 'Age', 'Disease', 'Multiple', 'Organ or Tissue Status', 'Allergy Intolerance', 'Compliance with Protocol', 'Risk Assessment', 'Pregnancy-related Activity', 'Diagnostic', 'Laboratory Examinations', 'Consent', 'Blood Donation', 'Enrollment in other studies', 'Pharmaceutical Substance or Drug', 'Capacity', 'Diet', 'Special Patient Characteristic', 'Non-Neoplasm Disease Stage', 'Researcher Decision', 'Data Accessible', 'Life Expectancy', 'Neoplasm Status', 'Literacy', 'Encounter', 'Exercise', 'Symptom', 'Receptor Status', 'Oral related', 'Ethnicity', 'Healthy', 'Disabilities', 'Device', 'Gender', 'Smoking Status', 'Sexual related', 'Nursing', 'Alcohol Consumer', 'Address', 'Education', 'Bedtime', 'Ethical Audit']

ctc_dic = {
    'Disease': '疾病',
    'Symptom': '症状(患者感受)',
    'Sign': '体征(医生检测）',
    'Pregnancy-related Activity': '怀孕相关',
    'Neoplasm Status': '肿瘤进展',
    'Non-Neoplasm Disease Stage': '疾病分期',
    'Allergy Intolerance': '过敏耐受',
    'Organ or Tissue Status': '器官组织状态',
    'Life Expectancy': '预期寿命',
    'Oral related': '口腔相关',
    'Pharmaceutical Substance or Drug': '药物',
    'Therapy or Surgery': '治疗或手术',
    'Device': '设备',
    'Nursing': '护理',
    'Diagnostic': '诊断',
    'Laboratory Examinations': '实验室检查',
    'Risk Assessment': '风险评估',
    'Receptor Status': '受体状态',
    'Age': '年龄',
    'Special Patient Characteristic': '特殊病人特征',
    'Literacy': '读写能力',
    'Gender': '性别',
    'Education': '教育情况',
    'Address': '居住情况',
    'Ethnicity': '种族',
    'Consent': '知情同意',
    'Enrollment in other studies': '参与其它试验',
    'Researcher Decision': '研究者决定',
    'Capacity': '能力',
    'Ethical Audit': '伦理审查',
    'Compliance with Protocol': '依存性',
    'Addictive Behavior': '成瘾行为',
    'Bedtime': '睡眠',
    'Exercise': '锻炼',
    'Diet': '饮食',
    'Alcohol Consumer': '酒精使用',
    'Sexual related': '性取向',
    'Smoking Status': '吸烟状况',
    'Blood Donation': '献血',
    'Encounter': '病例来源',
    'Disabilities': '残疾群体',
    'Healthy': '健康群体',
    'Data Accessible': '数据可及性',
    'Multiple': '含有多个类别',
}

print(len(ctc_dic))

ctc_train_datafile = '../../../../data/CHIP2023/ctc/CHIP-CTC_train.json'

with open(ctc_train_datafile, encoding='utf-8-sig') as f:
    chip_ctc = json.load(f)

# 加载temp
with open('../../../../data/CHIP2023/templates_augment.json', encoding='utf-8-sig') as f:
    temps = json.load(f)

print(len(chip_ctc))

# 统计chip_ctc中每个元素的'label'值有几种
# label_dict = {}
# for ctc in chip_ctc:
#     if ctc['label'] not in label_dict:
#         label_dict[ctc['label']] = 1
#     else:
#         label_dict[ctc['label']] += 1
#
# print(label_dict)
# print(len(label_dict))

chip_merge_datafile = '../../../../data/CHIP2023/chip/merge.json'

# 用读取jsonlines的方式读取chip_merge_datafile
with open(chip_merge_datafile, 'r', encoding='utf-8-sig') as f:
    chip_merge = f.readlines()

print(len(chip_merge))

# 判断chip_ctc中的元素中'text'指进行strip()后，是否存在chip_merge中，若存在则打flag为1
# flag = 0
# chip_merge_ctc为chip_merge中的元素"task_dataset"为"CHIP-CTC"的元素
chip_merge_ctc = []
for merge in chip_merge:
    merge = json.loads(merge)
    if merge['task_dataset'] == 'CHIP-CTC':
        chip_merge_ctc.append(merge)

chip_merge_ctc_str = str(chip_merge_ctc)
for ctc in chip_ctc:
    if ctc['text'].strip() in chip_merge_ctc_str:
        ctc['flag'] = 1

# 统计chip_ctc中flag为1的元素有多少
count = 0
for ctc in chip_ctc:
    if ctc.get('flag') == 1:
        count += 1

print(count)

# chip_ctc_flag0为chip_ctc中flag不为1的元素
chip_ctc_flag0 = []
for ctc in chip_ctc:
    if ctc.get('flag') != 1:
        chip_ctc_flag0.append(ctc)

chip_ctc_flag0 = random.sample(chip_ctc_flag0, 660)
ctc_add_list = []

for ctc in chip_ctc_flag0:
    samp_temp = random.choice(temps['CHIP-CTC'])

    target_str = ctc_dic[ctc['label']]

    instruction_str = samp_temp
    labels = list(ctc_dic.values())
    labels = [label for label in labels if label != target_str]
    # labels = 随机25-35个labels
    labels = random.sample(labels, random.randint(25, 35))
    # labels 把target_str放进去
    labels.append(target_str)
    random.shuffle(labels)
    instruction_str = instruction_str.replace('[INPUT_TEXT]', ctc['text'].strip()).replace('[LIST_LABELS]', '，'.join(labels)).replace('\\n', '\n')

    target_str = ctc_dic[ctc['label']]
    instruction_str = instruction_str.replace('\n答：', '')

    # 生成新的数据
    new_dic = {}
    new_dic['input'] = instruction_str
    new_dic["target"] = target_str
    new_dic["task_dataset"] = "CHIP-CTC"
    ctc_add_list.append(new_dic)

# ctc_add_list 存储，且为jsonlines格式
with open('../../../../data/CHIP2023/new_add/CHIP-CTC_aug.json', 'w', encoding='utf-8-sig') as f:
    for dic in ctc_add_list:
        json.dump(dic, f, ensure_ascii=False)
        f.write('\n')
