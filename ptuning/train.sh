source ptuning_config.sh


CUDA_VISIBLE_DEVICES=0 python3 main.py \
    --do_train \
    --train_file $train_file \
    --validation_file $validation_file \
    --prompt_column content \
    --response_column summary \
    --overwrite_cache \
    --model_name_or_path $model_name_or_path \
    --output_dir $output_dir \
    --overwrite_output_dir \
    --max_source_length 64 \
    --max_target_length 64 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 16 \
    --predict_with_generate \
    --max_steps 500 \
    --logging_steps 10 \
    --learning_rate $LR \
    --pre_seq_len $PRE_SEQ_LEN \
    --ptuning_checkpoint $ptuning_checkpoint \
    # --quantization_bit 4 \
    # --save_steps 1000 \

