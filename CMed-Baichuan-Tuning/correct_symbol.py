import json


with open('../../aug-prompt3-baichuan13b-chat-chip2023-lr2e4-bs1-grad16/pred-ckp24000-predB/generated_predictions.json', encoding='utf-8') as f:
    data = f.readlines()

# 把每一行中的json字符串转换成python字典
data = [json.loads(line) for line in data]
# 把每一行中'predict'字段的值';'替换为'；',':'替换为'：'
for line in data:
    line['predict'] = line['predict'].replace(';', '；').replace(':', '：')

# 把data新的内容写入到文件中
with open('../../aug-prompt3-baichuan13b-chat-chip2023-lr2e4-bs1-grad16/pred-ckp24000-predB/generated_predictions.jsonl', 'w', encoding='utf-8') as f:
    for line in data:
        json.dump(line, f, ensure_ascii=False)
        f.write('\n')

