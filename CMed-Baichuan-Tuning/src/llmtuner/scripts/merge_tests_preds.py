import json
import argparse

parser = argparse.ArgumentParser(description='offline prediction and evaluation')
parser.add_argument('-m', '--mode', type=str, default='offline')
parser.add_argument('-ckp', '--ckp_path', type=str)
args = parser.parse_args()
print(args.mode)
print(args.ckp_path)

if args.mode == 'online':
    # online test
    tests_file_path = '../../../data/CHIP2023/B_test.json'
    preds_file_path = '../../../../data/chip2023/{}/generated_predictions.jsonl'.format(args.ckp_path)

if args.mode == 'offline':
    # offline dev
    tests_file_path = '../../../data/CHIP2023/chip/dev.json'
    preds_file_path = '../../../../data/chip2023/{}/generated_predictions.jsonl'.format(args.ckp_path)

null = ''

res_lines = []
with open(tests_file_path, encoding='utf-8-sig') as f:
    for line in f.readlines():
        line = eval(line)
        # line = json.loads(line)
        # line = json.dumps(line, ensure_ascii=False)
        res_lines.append(line)
        # print(line)

preds = []
with open(preds_file_path, encoding='utf-8-sig') as f:
    for line in f.readlines():
        line = eval(line)
        preds.append(line)

print(len(res_lines))
print(len(preds))
for test, pred in zip(res_lines, preds):
    test['target'] = pred["predict"]

if args.mode == 'online':
    with open('../../../../data/chip2023/{}/test_predictions.json'.format(args.ckp_path), 'w', encoding='utf-8') as f:
        for line in res_lines:
            line = json.dumps(line, ensure_ascii=False)
            f.write(line + '\n')

if args.mode == 'offline':
    with open('../../../../data/chip2023/{}/dev_predictions.json'.format(args.ckp_path), 'w', encoding='utf-8') as f:
        for line in res_lines:
            line = json.dumps(line, ensure_ascii=False)
            f.write(line + '\n')
