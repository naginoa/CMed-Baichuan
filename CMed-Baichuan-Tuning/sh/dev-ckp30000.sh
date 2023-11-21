#!/bin/bash

cd /mnt/LLaMA-Efficient-Tuning

echo 123 >> /mnt/dev30000.txt

CUDA_VISIBLE_DEVICES=0 /root/miniconda3/envs/llama_etuning/bin/python /mnt/LLaMA-Efficient-Tuning/src/train_bash.py \
    --stage sft \
    --model_name_or_path ../models/chatglm2-6b/ \
    --do_predict \
    --dataset chip_dev \
    --template chatglm2 \
    --finetuning_type lora \
    --checkpoint_dir ../models/output/chatglm-lora/chip2023-lr2e4-bs4-grad4/checkpoint-30000 \
    --output_dir ../data/chip2023/chip2023-lr2e4-bs4-grad4/pred-ckp30000-dev \
    --per_device_eval_batch_size 8 \
    --bf16 \
    --predict_with_generate
	


