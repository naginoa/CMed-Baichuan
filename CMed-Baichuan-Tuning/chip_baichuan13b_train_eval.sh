CUDA_VISIBLE_DEVICES=0 python src/train_bash.py \
    --stage sft \
    --model_name_or_path ../models/baichuan-13b-chat/ \
    --do_train \
    --dataset chip_train_aug_prompt3 \
    --template baichuan \
    --finetuning_type lora \
    --lora_target W_pack,o_proj,gate_proj,up_proj,down_proj \
    --max_source_length 1536 \
    --output_dir ../models/output/baichuan-13b-chat-lora/aug-prompt3-chip2023-lr2e4-bs1-grad16 \
    --overwrite_cache \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 16 \
    --lr_scheduler_type cosine \
    --logging_steps 20 \
    --save_steps 250 \
    --learning_rate 2e-4 \
    --num_train_epochs 4 \
    --plot_loss \
    --bf16 \
    --flash_attn \
    --quantization_bit 4 \
    --overwrite_output_dir
