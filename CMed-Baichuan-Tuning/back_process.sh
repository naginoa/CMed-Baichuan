python merge_tests_preds.py -m online -ckp aug-prompt3-baichuan13b-chat-chip2023-lr2e4-bs1-grad16/pred-ckp23000-predB
python post_generate_process.py ../../../../data/chip2023/aug-prompt3-baichuan13b-chat-chip2023-lr2e4-bs1-grad16/pred-ckp23000-predB/test_predictions.json ../../../../data/chip2023/aug-prompt3-baichuan13b-chat-chip2023-lr2e4-bs1-grad16/pred-ckp23000-predB/results.json
