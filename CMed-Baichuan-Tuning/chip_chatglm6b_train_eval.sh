CUDA_VISIBLE_DEVICES=0 python src/train_bash.py \
    --stage sft \
    --model_name_or_path ../models/chatglm2-6b/ \
    --do_train \
    --dataset chip_train_prompt2 \
    --template chatglm2 \
    --finetuning_type lora \
    --lora_target query_key_value \
	--resume_from_checkpoint ../models/output/chatglm-lora/prompt2-chip2023-lr2e4-bs4-grad4/checkpoint-4500 \
    --output_dir ../models/output/chatglm-lora/prompt2-chip2023-lr2e4-bs4-grad4 \
    --overwrite_cache \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 20 \
    --save_steps 250 \
    --learning_rate 2e-4 \
    --num_train_epochs 1 \
    --plot_loss \
    --bf16 \
	--flash_attn \
    --overwrite_output_dir
	

CUDA_VISIBLE_DEVICES=0 python src/train_bash.py \
    --stage sft \
    --model_name_or_path ../models/chatglm2-6b/  \
    --do_predict \
    --dataset chip_dev_prompt2 \
    --template baichuan2 \
    --finetuning_type lora \
    --checkpoint_dir ../models/output/chatglm-lora/prompt2-chip2023-lr2e4-bs4-grad4/checkpoint-5000 \
    --output_dir ../data/chip2023/prompt2-chatglm6b-chip2023-lr2e4-bs4-grad4/pred-ckp5000-dev \
    --per_device_eval_batch_size 4 \
	--bf16 \
	--flash_attn \
    --predict_with_generate

