import json

# 读取文件内容
with open('test.txt', 'r') as f:
    data = json.load(f)

print(data)

