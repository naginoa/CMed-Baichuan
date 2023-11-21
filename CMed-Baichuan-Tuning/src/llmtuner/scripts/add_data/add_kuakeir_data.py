import json
import random


ir_train_query_file = '../../../../data/CHIP2023/ir/KUAKE-IR_train_query.txt'
ir_train_doc_file = '../../../../data/CHIP2023/ir/corpus.tsv'
ir_train_query_doc_file = '../../../../data/CHIP2023/ir/KUAKE-IR_train.tsv'

# query的id和query的dict
query_dict = {}

with open(ir_train_query_file, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        query_dict[line.split('\t')[0]] = line.split('\t')[1]

# doc的id和doc的dict
doc_dict = {}

with open(ir_train_doc_file, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        doc_dict[line.split('\t')[0]] = line.split('\t')[1]

# query和doc的id的dict
query_doc_id_dict = {}

with open(ir_train_query_doc_file, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        query_doc_id_dict[line.split('\t')[0]] = line.split('\t')[1]

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

# chip_merge_ir为chip_merge中的元素"task_dataset"为"KUAKE-IR"的元素
chip_merge_ir = []
for merge in chip_merge:
    merge = json.loads(merge)
    if merge['task_dataset'] == 'KUAKE-IR':
        chip_merge_ir.append(merge)

chip_merge_ir_str = str(chip_merge_ir)

# 判断query_dict中的每一个key-value对中value是否存在chip_merge_ir_str中，若存在则将该value值改为''
log_flag = 0
for key, value in query_dict.items():
    log_flag += 1
    if value in chip_merge_ir_str:
        query_dict[key] = ''

# 统计query_dict中value值为''的元素有多少
count = 0
for key, value in query_dict.items():
    if value == '':
        count += 1

print(count)
print(len(query_dict))
print('--- ---')

'''
print('len doc_dict', len(doc_dict))
# doc_dict 抽取其中的20000个元素
sorted_items = sorted(doc_dict.items())
selected_items = random.sample(sorted_items, 20000)
doc_dict = {k: v for k, v in selected_items}

# 判断doc_dict中的每一个key-value对中value是否存在chip_merge_ir_str中，若存在则将该value值改为''
for key, value in doc_dict.items():
    if log_flag % 1000 == 0:
        print('---', log_flag)
    if value in chip_merge_ir_str:
        doc_dict[key] = ''

# 统计doc_dict中value值为''的元素有多少
count = 0
for key, value in doc_dict.items():
    if value == '':
        count += 1

print(count)
print(len(doc_dict))

# 将query_dict和doc_dict中value值为''的元素删除
for key in list(query_dict.keys()):
    if query_dict[key] == '':
        query_dict.pop(key)

for key in list(query_dict.keys()):
    if query_dict[key] == '':
        query_dict.pop(key)

# 将query_dict写入json文件
with open('../../../../data/CHIP2023/ir/KUAKE-IR_train_query_filter.json', 'w', encoding='utf-8-sig') as f:
    json.dump(query_dict, f, ensure_ascii=False)

# 将doc_dict写入json文件
with open('../../../../data/CHIP2023/ir/KUAKE-IR_train_doc_filter.json', 'w', encoding='utf-8-sig') as f:
    json.dump(doc_dict, f, ensure_ascii=False)
'''

# query_dict读取json文件
with open('../../../../data/CHIP2023/ir/KUAKE-IR_train_query_filter.json', 'r', encoding='utf-8-sig') as f:
    query_dict = json.load(f)

# doc_dict读取json文件
with open('../../../../data/CHIP2023/ir/KUAKE-IR_train_doc_filter.json', 'r', encoding='utf-8-sig') as f:
    doc_dict = json.load(f)

print(len(query_dict))
print(len(doc_dict))

# 加载temp
with open('../../../../data/CHIP2023/templates_augment.json', encoding='utf-8-sig') as f:
    temps = json.load(f)

pos_query_doc = []
flag = 0
sample_num = 500
# 判断doc_dict中的每一个key-value对中key是否存在于query_doc_id_dict中，若存在则将flag+1
for key, value in doc_dict.items():
    if len(pos_query_doc) >= sample_num:
        break
    if key in query_doc_id_dict.values():
        flag += 1
        # print(key)
        #  doc_dict中的key对应的query_doc_id_dict的value值，那么query_doc_id_dict中的key如何获取
        for k, v in query_doc_id_dict.items():
            if v == key:
                # print(k, v)
                if k not in query_dict.keys():
                    continue
                pos_query_doc.append([(k, query_dict[k]), (v, doc_dict[v])])

neg_query_doc = []
# 从query中抽取1个query，从doc中抽取1个doc
while len(neg_query_doc) < sample_num:
    query_sample = random.sample(list(query_dict.items()), 1)
    doc_sample = random.sample(list(doc_dict.items()), 1)

    # 如果{query_sample[0]: doc_sample[0]}不在query_doc_id_dict中，则将其加入neg_query_doc
    if {query_sample[0]: doc_sample[0]} not in query_doc_id_dict.items():
        neg_query_doc.append([query_sample[0], doc_sample[0]])

print(len(pos_query_doc))
print(pos_query_doc[:5])

print(len(neg_query_doc))
print(neg_query_doc[:5])

ir_add_lines = []

for p_q_d in pos_query_doc:
    samp_temp = random.choice(temps["KUAKE-IR"])
    print(samp_temp)
    answer_choices = ["相关", "不相关"]

    instruction_str = samp_temp
    instruction_str = instruction_str.replace("[INPUT_TEXT_1]", p_q_d[0][1]).replace("[INPUT_TEXT_2]", p_q_d[1][1]).\
        replace("[ANSWER_1]", answer_choices[0]).replace("[LIST_LABELS]", '，'.join(answer_choices)).replace('\\n', '\n')

    target_str = answer_choices[0]

    instruction_str = instruction_str.replace('\n答：', '').replace(' 答：', '')

    new_dic = {
        "input": instruction_str,
        "target": target_str,
        "task_dataset": "KUAKE-IR"
    }
    ir_add_lines.append(new_dic)

for n_q_d in neg_query_doc:
    samp_temp = random.choice(temps["KUAKE-IR"])
    print(samp_temp)
    answer_choices = ["相关", "不相关"]

    instruction_str = samp_temp
    instruction_str = instruction_str.replace("[INPUT_TEXT_1]", n_q_d[0][1]).replace("[INPUT_TEXT_2]", n_q_d[1][1]).\
        replace("[ANSWER_1]", answer_choices[1]).replace("[LIST_LABELS]", '，'.join(answer_choices)).replace('\\n', '\n')

    target_str = answer_choices[1]

    instruction_str = instruction_str.replace('\n答：', '').replace(' 答：', '')

    new_dic = {
        "input": instruction_str,
        "target": target_str,
        "task_dataset": "KUAKE-IR"
    }
    ir_add_lines.append(new_dic)

random.shuffle(ir_add_lines)
print(len(ir_add_lines))
print(random.sample(ir_add_lines, 5))

# 将ir_add_lines存储为jsonlines
with open('../../../../data/CHIP2023/new_add/KUAKE-IR_aug.json', 'w', encoding='utf-8') as f:
    for line in ir_add_lines:
        json.dump(line, f, ensure_ascii=False)
        f.write('\n')
