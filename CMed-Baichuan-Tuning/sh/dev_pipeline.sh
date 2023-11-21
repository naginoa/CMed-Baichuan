#!/bin/bash
PARAMS_PATH='chip2023-lr2e4-bs4-grad4/'
#TRAIN_CKP='checkpoint-30000'
#CKP_PATH='pred-ckp30000-dev'

cd /mnt/LLaMA-Efficient-Tuning

/root/miniconda3/envs/llama_etuning/bin/python /mnt/LLaMA-Efficient-Tuning/src/train_bash.py \
    --stage sft \
    --model_name_or_path ../models/chatglm2-6b/ \
    --do_predict \
    --dataset chip_dev \
    --template chatglm2 \
    --finetuning_type lora \
    --checkpoint_dir ../models/output/chatglm-lora/$PARAMS_PATH$TRAIN_CKP \
    --output_dir ../data/chip2023/$PARAMS_PATH$CKP_PATH \
    --per_device_eval_batch_size 8 \
    --predict_with_generate

cd /mnt/LLaMA-Efficient-Tuning/src/llmtuner/scripts

#/root/miniconda3/envs/llama_etuning/bin/python merge_tests_preds.py -m offline -ckp $PARAMS_PATH$CKP_PATH

/root/miniconda3/envs/llama_etuning/bin/python post_generate_process.py ../../../../data/chip2023/$PARAMS_PATH$CKP_PATH/dev_predictions.json ../../../../data/chip2023/$PARAMS_PATH$CKP_PATH/dev_results.json

/root/miniconda3/envs/llama_etuning/bin/python evaluate.py ../../../../data/chip2023/$PARAMS_PATH$CKP_PATH/dev_results.json ../../../../data/chip2023/$PARAMS_PATH$CKP_PATH/eval_result.json

