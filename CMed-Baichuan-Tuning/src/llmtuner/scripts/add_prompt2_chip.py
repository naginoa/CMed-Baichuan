import random
import json


filepath = '../../../data/CHIP2023/'
null = ''

type_prompt_dic = {
    'CMeEE-V2': '进行中文医学命名实体识别任务，任务类型为实体识别\n',
    'CMeIE-V2': '进行中文医学文本实体关系抽取任务，任务类型为关系抽取\n',
    'CMedCausal': '进行医疗因果实体关系抽取任务，任务类型为关系抽取\n',
    'IMCS-V2-NER': '进行智能对话诊疗命名实体识别任务，任务类型为实体识别\n',
    'IMCS-V2-SR': '进行智能对话诊疗症状识别任务，任务类型为实体识别加分类\n',
    'IMCS-V2-MRG': '进行智能对话诊疗医疗报告生成任务，任务类型为生成\n',
    'IMCS-V2-DAC': '进行智能对话诊疗对话意图识别任务，任务类型为分类\n',
    'CHIP-CDEE': '进行临床发现事件抽取任务，任务类型为事件抽取\n',
    'CHIP-CDN': '进行临床术语标准化任务，任务类型为归一化\n',
    'KUAKE-IR': "进行医学段落检索任务，任务类型为检索\n",
    'CHIP-CTC': "进行临床试验筛选标准短文本分类任务，任务类型为分类\n",
    'KUAKE-QIC': "进行医疗搜索检索词意图分类任务，任务类型为分类\n",
    'CHIP-MDCFNPC': '进行医疗对话临床发现阴阳性判别任务，任务类型为实体识别加分类\n',
    'CHIP-STS': '进行疾病问答迁移学习任务，任务类型为匹配\n',
    'KUAKE-QTR': '进行医疗搜索查询词-页面标题相关性判断任务，任务类型为匹配\n',
    'KUAKE-QQR': '进行医疗搜索查询词-查询词相关性判断任务，任务类型为匹配\n',
    'MedDG': '进行蕴含实体的中文医疗对话生成任务，任务类型为生成\n',
    'Text2DT': '进行医疗文本诊疗决策树抽取任务，任务类型为生成\n'
}

# 加载temp
# with open('../../../data/CHIP2023/templates_augment.json', encoding='utf-8-sig') as f:
#     temps = json.load(f)
# print(len(temps.keys()))
# print(len(type_prompt_dic.keys()))

res_lines = []

with open(filepath + '/chip/train.json', encoding='utf-8') as f1:
    for line in f1.readlines():
        line = eval(line)

        if line['task_dataset'] == 'CMeEE-V2':
            choices_explanation = {
                '疾病': '指患病、综合征、中毒、受伤、器官损伤等',
                '临床表现': '指某症状或体征，如发热、剧咳等',
                '医疗程序': '指检查、治疗或预防等程序，如免疫学方法检测等',
                '医疗设备': '指检查或治疗设备',
                '药物': '即用以预防、治疗及诊断疾病的物质',
                '医学检验项目': '如渗透压、红细胞、Ig水平和组成成分等',
                '身体部位': '指身体物质或部位，如脾脏、手等部位或胃酸、染色体等物质',
                '医院科室': '如外科、眼科等',
                '微生物类': '包括细菌、病毒、真菌等，如军团菌、HIV等'
            }
            line_expl = [ce+'实体'+choices_explanation.get(ce) for ce in choices_explanation if ce in line['answer_choices']]
            # 减少字数，随机抽取2到3个解释
            line_expl = random.sample(line_expl, random.randint(2, 3))
            explain_prompt = '；'.join(line_expl)

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CMeEE-V2') + line['input'] + '\n实体解释如下:\n' + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'CMeIE-V2':
            explain_prompt = '头实体和尾实体之间存在上述提到的某种关系'

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CMeIE-V2') + line[
                'input'] + '\n头尾实体解释如下:\n' + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'CMedCausal':

            cmed_exp = [
                '因果关系：胃肠道功能紊乱是吸收能力变差的一个直接原因，吸收能力变差是胃肠功能紊乱的直接结果。',
                '条件关系：对阿莫西林过敏的患者不可以使用,服用阿莫西林可能会引起皮疹；其中，“对阿莫西林过敏”是服用阿莫西林导致皮疹的条件。',
                '上下位关系：阿尔茨海默症是精神类疾病的一种，因此与精神类疾病构成了上下位关系。'
            ]

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CMedCausal') + line[
                'input'] + '\n关系举例如下:\n' + random.choice(cmed_exp)
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'IMCS-V2-NER':
            choices_explanation = {
                '疾病': '指患病、综合征、中毒、受伤、器官损伤等',
                '医疗操作': '，如雾化和输液等',
                '具体的药物名称': '，如多潘立酮、安乐宝等',
                '药物类别': '，如退烧药、益生菌等',
                '医学检查检验': '，如支原体、经皮黄疸指数等',
            }
            line_expl = [ce + '实体' + choices_explanation.get(ce) for ce in choices_explanation if
                         ce in line['answer_choices']]
            # 减少字数，随机抽取2个解释
            line_expl = random.sample(line_expl, 2)
            explain_prompt = '；'.join(line_expl)

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('IMCS-V2-NER') + line[
                'input'] + '\n实体解释如下:\n' + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'IMCS-V2-SR':
            explain_prompt = '该任务需要先进行实体识别，然后判断其实体的阴阳性\n'

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('IMCS-V2-SR') + explain_prompt + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'IMCS-V2-MRG':
            choices_explanation = {
                '主诉': '指患者感受最主要的痛苦，就诊最主要的原因或最明显的症状或（和）体征、性质，以及持续时间。',
                '现病史': '指记述患者病后的全过程，即发生、发展、演变和诊治经过',
                '辅助检查': '指通过医学设备进行身体检查，如血常规、胸片等',
                '既往史': '指既往的健康状况和过去曾经患过的疾病',
                '诊断': '指从医学角度对人们的精神和体质状态作出的判断，如发热待查、黄疸等',
                '建议': '指给出的后续治疗方案建议，如予消炎止咳药服用等'
            }
            line_expl = [ce + choices_explanation.get(ce) for ce in choices_explanation]
            # 减少字数，随机抽取3个解释
            line_expl = random.sample(line_expl, 3)
            explain_prompt = '；'.join(line_expl)

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('IMCS-V2-MRG') + line['input'] + '\n解释如下:\n' + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'IMCS-V2-DAC':
            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('IMCS-V2-DAC') + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'CHIP-CDEE':
            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CHIP-CDEE') + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'CHIP-CDN':
            explain_prompt = '。ICD指是WHO制定的国际统一的疾病分类方法\n'

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CHIP-CDN') + line['input'] + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'KUAKE-IR':
            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('KUAKE-IR') + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        else:
            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get(line['task_dataset']) + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)


with open("../../../data/chip2023_train_prompt2.json", "w") as f:
    json.dump(res_lines, f, ensure_ascii=False, indent=2)
    print("加载入文件完成...")

res_lines = []

with open(filepath + 'A_test.json', encoding='utf-8') as f1:
    for line in f1.readlines():
        line = eval(line)

        if line['task_dataset'] == 'CMeEE-V2':
            choices_explanation = {
                '疾病': '指患病、综合征、中毒、受伤、器官损伤等',
                '临床表现': '指某症状或体征，如发热、剧咳等',
                '医疗程序': '指检查、治疗或预防等程序，如免疫学方法检测等',
                '医疗设备': '指检查或治疗设备',
                '药物': '即用以预防、治疗及诊断疾病的物质',
                '医学检验项目': '如渗透压、红细胞、Ig水平和组成成分等',
                '身体部位': '指身体物质或部位，如脾脏、手等部位或胃酸、染色体等物质',
                '医院科室': '如外科、眼科等',
                '微生物类': '包括细菌、病毒、真菌等，如军团菌、HIV等'
            }
            line_expl = [ce+'实体'+choices_explanation.get(ce) for ce in choices_explanation if ce in line['answer_choices']]
            # 减少字数，随机抽取2到3个解释
            line_expl = random.sample(line_expl, random.randint(2, 3))
            explain_prompt = '；'.join(line_expl)

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CMeEE-V2') + line['input'] + '\n实体解释如下:\n' + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'CMeIE-V2':
            explain_prompt = '头实体和尾实体之间存在上述提到的某种关系'

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CMeIE-V2') + line[
                'input'] + '\n头尾实体解释如下:\n' + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'CMedCausal':

            cmed_exp = [
                '因果关系：胃肠道功能紊乱是吸收能力变差的一个直接原因，吸收能力变差是胃肠功能紊乱的直接结果。',
                '条件关系：对阿莫西林过敏的患者不可以使用,服用阿莫西林可能会引起皮疹；其中，“对阿莫西林过敏”是服用阿莫西林导致皮疹的条件。',
                '上下位关系：阿尔茨海默症是精神类疾病的一种，因此与精神类疾病构成了上下位关系。'
            ]

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CMedCausal') + line[
                'input'] + '\n关系举例如下:\n' + random.choice(cmed_exp)
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'IMCS-V2-NER':
            choices_explanation = {
                '疾病': '指患病、综合征、中毒、受伤、器官损伤等',
                '医疗操作': '，如雾化和输液等',
                '具体的药物名称': '，如多潘立酮、安乐宝等',
                '药物类别': '，如退烧药、益生菌等',
                '医学检查检验': '，如支原体、经皮黄疸指数等',
            }
            line_expl = [ce + '实体' + choices_explanation.get(ce) for ce in choices_explanation if
                         ce in line['answer_choices']]
            # 减少字数，随机抽取2个解释
            line_expl = random.sample(line_expl, 2)
            explain_prompt = '；'.join(line_expl)

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('IMCS-V2-NER') + line[
                'input'] + '\n实体解释如下:\n' + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'IMCS-V2-SR':
            explain_prompt = '该任务需要先进行实体识别，然后判断其实体的阴阳性\n'

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('IMCS-V2-SR') + explain_prompt + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'IMCS-V2-MRG':
            choices_explanation = {
                '主诉': '指患者感受最主要的痛苦，就诊最主要的原因或最明显的症状或（和）体征、性质，以及持续时间。',
                '现病史': '指记述患者病后的全过程，即发生、发展、演变和诊治经过',
                '辅助检查': '指通过医学设备进行身体检查，如血常规、胸片等',
                '既往史': '指既往的健康状况和过去曾经患过的疾病',
                '诊断': '指从医学角度对人们的精神和体质状态作出的判断，如发热待查、黄疸等',
                '建议': '指给出的后续治疗方案建议，如予消炎止咳药服用等'
            }
            line_expl = [ce + choices_explanation.get(ce) for ce in choices_explanation]
            # 减少字数，随机抽取3个解释
            line_expl = random.sample(line_expl, 3)
            explain_prompt = '；'.join(line_expl)

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('IMCS-V2-MRG') + line['input'] + '\n解释如下:\n' + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'IMCS-V2-DAC':
            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('IMCS-V2-DAC') + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'CHIP-CDEE':
            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CHIP-CDEE') + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'CHIP-CDN':
            explain_prompt = '。ICD指是WHO制定的国际统一的疾病分类方法\n'

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CHIP-CDN') + line['input'] + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'KUAKE-IR':
            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('KUAKE-IR') + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        else:
            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get(line['task_dataset']) + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

with open("../../../data/chip2023_test_prompt2.json", "w") as f:
    json.dump(res_lines, f, ensure_ascii=False, indent=2)
    print("加载入文件完成...")

res_lines = []

with open(filepath + '/chip/dev.json', encoding='utf-8') as f1:
    for line in f1.readlines():
        line = eval(line)

        if line['task_dataset'] == 'CMeEE-V2':
            choices_explanation = {
                '疾病': '指患病、综合征、中毒、受伤、器官损伤等',
                '临床表现': '指某症状或体征，如发热、剧咳等',
                '医疗程序': '指检查、治疗或预防等程序，如免疫学方法检测等',
                '医疗设备': '指检查或治疗设备',
                '药物': '即用以预防、治疗及诊断疾病的物质',
                '医学检验项目': '如渗透压、红细胞、Ig水平和组成成分等',
                '身体部位': '指身体物质或部位，如脾脏、手等部位或胃酸、染色体等物质',
                '医院科室': '如外科、眼科等',
                '微生物类': '包括细菌、病毒、真菌等，如军团菌、HIV等'
            }
            line_expl = [ce+'实体'+choices_explanation.get(ce) for ce in choices_explanation if ce in line['answer_choices']]
            # 减少字数，随机抽取2到3个解释
            line_expl = random.sample(line_expl, random.randint(2, 3))
            explain_prompt = '；'.join(line_expl)

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CMeEE-V2') + line['input'] + '\n实体解释如下:\n' + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'CMeIE-V2':
            explain_prompt = '头实体和尾实体之间存在上述提到的某种关系'

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CMeIE-V2') + line[
                'input'] + '\n头尾实体解释如下:\n' + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'CMedCausal':

            cmed_exp = [
                '因果关系：胃肠道功能紊乱是吸收能力变差的一个直接原因，吸收能力变差是胃肠功能紊乱的直接结果。',
                '条件关系：对阿莫西林过敏的患者不可以使用,服用阿莫西林可能会引起皮疹；其中，“对阿莫西林过敏”是服用阿莫西林导致皮疹的条件。',
                '上下位关系：阿尔茨海默症是精神类疾病的一种，因此与精神类疾病构成了上下位关系。'
            ]

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CMedCausal') + line[
                'input'] + '\n关系举例如下:\n' + random.choice(cmed_exp)
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'IMCS-V2-NER':
            choices_explanation = {
                '疾病': '指患病、综合征、中毒、受伤、器官损伤等',
                '医疗操作': '，如雾化和输液等',
                '具体的药物名称': '，如多潘立酮、安乐宝等',
                '药物类别': '，如退烧药、益生菌等',
                '医学检查检验': '，如支原体、经皮黄疸指数等',
            }
            line_expl = [ce + '实体' + choices_explanation.get(ce) for ce in choices_explanation if
                         ce in line['answer_choices']]
            # 减少字数，随机抽取2个解释
            line_expl = random.sample(line_expl, 2)
            explain_prompt = '；'.join(line_expl)

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('IMCS-V2-NER') + line[
                'input'] + '\n实体解释如下:\n' + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'IMCS-V2-SR':
            explain_prompt = '该任务需要先进行实体识别，然后判断其实体的阴阳性\n'

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('IMCS-V2-SR') + explain_prompt + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'IMCS-V2-MRG':
            choices_explanation = {
                '主诉': '指患者感受最主要的痛苦，就诊最主要的原因或最明显的症状或（和）体征、性质，以及持续时间。',
                '现病史': '指记述患者病后的全过程，即发生、发展、演变和诊治经过',
                '辅助检查': '指通过医学设备进行身体检查，如血常规、胸片等',
                '既往史': '指既往的健康状况和过去曾经患过的疾病',
                '诊断': '指从医学角度对人们的精神和体质状态作出的判断，如发热待查、黄疸等',
                '建议': '指给出的后续治疗方案建议，如予消炎止咳药服用等'
            }
            line_expl = [ce + choices_explanation.get(ce) for ce in choices_explanation]
            # 减少字数，随机抽取3个解释
            line_expl = random.sample(line_expl, 3)
            explain_prompt = '；'.join(line_expl)

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('IMCS-V2-MRG') + line['input'] + '\n解释如下:\n' + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'IMCS-V2-DAC':
            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('IMCS-V2-DAC') + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'CHIP-CDEE':
            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CHIP-CDEE') + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'CHIP-CDN':
            explain_prompt = '。ICD指是WHO制定的国际统一的疾病分类方法\n'

            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('CHIP-CDN') + line['input'] + explain_prompt
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        elif line['task_dataset'] == 'KUAKE-IR':
            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get('KUAKE-IR') + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)

        else:
            new_dic = {}
            new_dic["instruction"] = type_prompt_dic.get(line['task_dataset']) + line['input']
            new_dic['input'] = ''
            new_dic['output'] = line['target']

            res_lines.append(new_dic)


with open("../../../data/chip2023_dev_prompt2.json", "w") as f:
    json.dump(res_lines, f, ensure_ascii=False, indent=2)
    print("加载入文件完成...")