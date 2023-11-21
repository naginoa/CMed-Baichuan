import json
import random


text2dt_train_datafile = '../../../../data/CHIP2023/text2dt/Text2DT_train.json'
with open(text2dt_train_datafile, encoding='utf-8-sig') as f:
    text2dt_train = json.load(f)

text2dt_dev_datafile = '../../../../data/CHIP2023/text2dt/Text2DT_dev.json'
with open(text2dt_dev_datafile, encoding='utf-8-sig') as f:
    text2dt_dev = json.load(f)

print(len(text2dt_train))
print(len(text2dt_dev))
