import random
import json


filepath = '../../../data/CHIP2023/'
null = ''

# 加载temp
# with open(filepath + 'templates_augment.json', encoding='utf-8-sig') as f:
#     temps = json.load(f)
# print(temps)

res_lines = []

# with open(filepath + '/prompt_data2/train.json', encoding='utf-8') as f1:
#     for line in f1.readlines():
#         line = eval(line)
#         # if line['task_dataset'] == "CMeEE-V2":
#         #     samp_temp = random.choice(temps['CMeEE-V2'])
#         #     samp_temp = samp_temp.replace('[INPUT_TEXT]', line['input']).replace('[LIST_LABELS]', '')
#         #     print(samp_temp)
#         # print('--------')
#         # print(line['input'])
#         # print(line['target'])
#
#         new_dic = {}
#         new_dic["instruction"] = line["instruction"] + '\n' + line['input']
#         new_dic['input'] = ''
#         new_dic['output'] = line['target']
#
#         line = json.dumps(line, ensure_ascii=False)
#         res_lines.append(new_dic)
#
# with open("../../../data/chip2023_train_prompt3.json", "w") as f:
#     json.dump(res_lines, f, ensure_ascii=False, indent=2)
#     print("加载入文件完成...")
#
# res_lines = []
#
# with open(filepath + '/prompt_data2/Atest.json', encoding='utf-8') as f1:
#     for line in f1.readlines():
#         line = eval(line)
#         # if line['task_dataset'] == "CMeEE-V2":
#         #     samp_temp = random.choice(temps['CMeEE-V2'])
#         #     samp_temp = samp_temp.replace('[INPUT_TEXT]', line['input']).replace('[LIST_LABELS]', '')
#         #     print(samp_temp)
#         # print('--------')
#         # print(line['input'])
#         # print(line['target'])
#
#         new_dic = {}
#         new_dic["instruction"] = line["instruction"] + '\n' + line['input']
#         new_dic['input'] = ''
#         new_dic['output'] = line['target']
#
#         line = json.dumps(line, ensure_ascii=False)
#         res_lines.append(new_dic)

# with open("../../../data/chip2023_test_prompt3.json", "w") as f:
#     json.dump(res_lines, f, ensure_ascii=False, indent=2)
#     print("加载入文件完成...")

# res_lines = []
#
# with open(filepath + '/prompt_data2/dev.json', encoding='utf-8') as f1:
#     for line in f1.readlines():
#         line = eval(line)
#         # if line['task_dataset'] == "CMeEE-V2":
#         #     samp_temp = random.choice(temps['CMeEE-V2'])
#         #     samp_temp = samp_temp.replace('[INPUT_TEXT]', line['input']).replace('[LIST_LABELS]', '')
#         #     print(samp_temp)
#         # print('--------')
#         # print(line['input'])
#         # print(line['target'])
#
#         new_dic = {}
#         new_dic["instruction"] = line["instruction"] + '\n' + line['input']
#         new_dic['input'] = ''
#         new_dic['output'] = line['target']
#         line = json.dumps(line, ensure_ascii=False)
#         res_lines.append(new_dic)
#
# with open("../../../data/chip2023_dev_prompt3.json", "w") as f:
#     json.dump(res_lines, f, ensure_ascii=False, indent=2)
#     print("加载入文件完成...")


# with open(filepath + 'A_test.json', encoding='utf-8') as f1:
#     for line in f1.readlines():
#         line = eval(line)
#
#         new_dic = {}
#         new_dic["instruction"] = line['input']
#         new_dic['input'] = ''
#         new_dic['output'] = line['target']
#         line = json.dumps(line, ensure_ascii=False)
#         res_lines.append(new_dic)
#
# with open("../../../data/chip2023_test.json", "w") as f:
#     json.dump(res_lines, f, ensure_ascii=False, indent=2)
#     print("加载入文件完成...")

res_lines = []

prompt_dict = {
    "CMeEE-V2": "任务类型：命名实体识别任务一\n任务描述：从指定的文本中识别给定类型的实体\n实体解释：医疗设备：用于医疗诊断、治疗或监测的工具、仪器或设备\n临床表现：患者的症状、体征和其他临床特征\n微生物类：包括细菌、病毒、真菌和寄生虫等微生物体\n医疗程序：医疗操作、过程或程序\n身体部位：人体的具体部位或器官\n疾病：人体异常状况或功能障碍引起的身或心理异常状态\n药物：治疗、预或缓解疾病的化学物质或药剂\n医学检验项目：评估、诊断监测患者健康状况的医学检查方法或测试项目\n输出格式：上述句子中的实体包含：实体类型：实体1、实体2",
    "IMCS-V2-NER": "任务类型：命名实体识别任务一\n任务描述：从指定的文本中识别给定类型的实体\n实体解释：医疗设备：用于医疗诊断、治疗或监测的工具、仪器或设备\n临床表现：患者的症状、体征和其他临床特征\n微生物类：包括细菌、病毒、真菌和寄生虫等微生物体\n医疗程序：医疗操作、过程或程序\n身体部位：人体的具体部位或器官\n疾病：人体异常状况或功能障碍引起的身或心理异常状态\n药物：治疗、预或缓解疾病的化学物质或药剂\n医学检验项目：评估、诊断监测患者健康状况的医学检查方法或测试项目\n输出格式：上述句子中的实体包含：实体类型：实体1、实体2",
    "CMeIE-V2": "任务类型：实体关系抽取任务\n任务描述：从指定的文本中识别出实体的语义关系，如影像学检查、多发群体等。\n头尾实体解释：头实体：在关系中作为主体或起始点的实体。\n尾实体：在关系中作为客体或结束点的实体。\n输出示例：具有预后状况关系的头尾实体对如下：头实体为川崎病，尾实体为良好",
    "CHIP-CDN": "任务类型：文本匹配任务\n任务描述：把给定的原词与选项中的词语进行匹配，找出与原词匹配的选项，匹配的选项可以有多个，如果没有匹配的选项，则输出：没有对应的标准化实体。",
    "CHIP-CDEE": "任务类型：临床事件生成任务\n任务描述：现在你是一名医生，请根据患者病历记录写出病历记录中的临床发生事件，包括主体词，发生状态，描述词、解剖部位。\n属性解释：\n主体词：表示事件发生的主体或对象。例如，在“狗咬伤”中，主体词是“狗”。\n发生状态：表示事件发生的状态或情况。例如，在“咬伤”中，发生状态是“咬伤”。\n描述词：用于描述事件的性质、程度、影响等。例如，在“严重咬伤”中，描述词是“严重”。\n解剖部位：表示事件发生的具体位置或部位。例如，在“咬伤手”中，解剖部位是“手”。\n输出示例：上述句子中的临床发现事件如下：主体词：；发生状态：；描述词：；解剖部位：",
    "CHIP-MDCFNPC": "任务类型：临床发现实体的阴阳性判断任务\n任务描述：文中指出了一些临床发现实体，请根据医患对话，判断这些临床发现实体是属于阴性还是阳性\n输出格式：当前对话中的症状及其阴阳性判断为：实体：阴阳性",
    "IMCS-V2-SR": "任务类型：症状实体抽取和阴阳性判断任务\n任务描述：症状实体指患者的主观感受或可观察到的体征。对阴阳性标签说明如下：“患有该症状”是指已有症状疾病或者假设未来可能发生的疾病等；“没有患有该症状”是指未患有症状疾病，“无法根据上下文确定病人是否患有该症状”指没有回答、不知道、回答不明确或者模棱两可不好推断",
    "IMCS-V2-DAC": "任务类别：意图识别任务\n任务描述：在该任务中，你是一名实习医生，请根据医患对话，确定对话的最后一句中说话人的意图。",
    "CHIP-CTC": "任务类别：文本分类任务\n任务描述：在这个任务中，你需要根据给定的文本和选项来判断该文本表达的临床试验筛选标准类型是哪个选项。这个任务需要你对文本进行理解和分析，并选择正确的答案。",
    "CHIP-STS": "任务类型：问题相似任务\n任务描述：在该任务中，你是一名医生，请判断给出的两个问句的医学含义是否相同，如果相同则回答“是的”，否则回答“不是”",
    "KUAKE-IR": "任务类型：问答相关性任务\n任务描述：判断给定的问题搜索和答案是否相关",
    "KUAKE-QIC": "任务类型：意图识别任务\n任务描述：给定一个句子或搜索词，需要从给定的意图类型选项中选择正确的意图类型。\n任务示例：问：对于给定的医学搜索词，请选择正确的意图类型：\n弱精症常见征兆\n可选意图：治疗方案，病情诊断，疾病描述，功效作用，医疗费用，病因分析，就医建议，后果表述，疾病表述，指标解读，注意事项, 答：疾病表述",
    "KUAKE-QQR": "任务类型：语义关系抽取任务\n任务描述：请判断给定的两个搜索查询之间的语义关系，并选择正确的关系类型。\n语义关联关系选项解释：\n“完全一致”这个概念意味着两个搜索词的语义是完全相同的，即它们包含的信息没有任何差异。\n“后者是前者的语义子集”这个概念意味着第二个搜索词的语义范围完全包含在第一个搜索词的语义范围之内。\n“后者是前者的语义父集”这个概念意味着第一个搜索词的语义范围完全包含在第二个搜索词的语义范围之内。\n“语义无直接关联”：意味着两个搜索词之间没有明显的语义联系，即它们包含的信息没有交集或者关联度很低。",
    "KUAKE-QTR": "任务类型：语义相似度判断任务\n相似度选项解释：”完全不匹配“意味着两个句子没有任何相似之处，”很少匹配有一些参考价值“意味着有一些小的相似之处，”部分匹配“意味着有一些显著的相似之处，但不完全相同，”完全匹配“则意味着两个句子的语义几乎完全相同。",
    "MedDG": "任务类型：医疗咨询对话任务\n任务描述：在这个任务里，假如你是一名医生，请你根据医患对话，对患者的询问进行回复。要求需要根据患者的描述和症状，给出相应的建议和治疗方案。",
    "Text2DT": "任务类型：生成诊断决策树任务\n任务描述：根据给定医学指南文本，创建一个二叉树，包含条件节点和决策节点，同时捕捉核心实体和关系；条件节点用于判断，根据结果指向左侧或右侧子节点进行下一步决策。",
    "CMedCausal": "任务类型： 医学文本三元组抽取任务\n任务描述：需要根据给定的医学文本，识别并抽取其中的医学概念（实体）以及它们之间的关系，形成三元组。请注意”文本抽取的条件关系三元组“属性包括头实体和尾三元组，尾三元组包括头实体、尾实体、关系。”文本抽取的因果关系三元组“和”文本抽取的上下位关系三元组“的属性包括头实体、尾实体。\n输出格式：根据给定的文本抽取的因果关系三元组如下：头实体：；尾实体：\n根据给定的文本抽取的条件关系三元组如下：\n头实体：；尾三元组：头实体：；尾实体：；关系：\n根据给定的文本抽取的上下位关系三元组如下：头实体：；尾实体：",
    "IMCS-V2-MRG": "任务类型：诊断报告生成任务\n任务描述：这个任务中，你是一名医生。请你根据医患对话生成对患者的诊断报告。要求准确、客观、规范。\n输出格式示例：上述问诊对话的诊疗报告如下：\n主诉：流涕咳嗽两天。\n现病史：患儿两天前出现咳嗽流涕症状，口服阿莫西林和小儿化痰止咳颗粒和美愈伪麻颗粒治疗，目前症状无明显改善。\n辅助检查：暂缺。\n既往史：不详。\n诊断：小儿支气管炎。\n建议：清理鼻腔、医院就诊、完善相关检查，合理用药。"
}

res_lines = []

with open(filepath + 'B_test.json', encoding='utf-8') as f1:
    for line in f1.readlines():
        line = eval(line)

        prompt_str = prompt_dict[line['task_dataset']]

        new_dic = {}
        new_dic["instruction"] = prompt_str + '\n' + line['input']
        new_dic['input'] = ''
        new_dic['output'] = line['target']

        line = json.dumps(line, ensure_ascii=False)
        res_lines.append(new_dic)

with open("../../../data/chip2023_predB_prompt3.json", "w") as f:
    json.dump(res_lines, f, ensure_ascii=False, indent=2)
    print("加载入文件完成...")
