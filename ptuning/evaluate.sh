source ptuning_config.sh

CUDA_VISIBLE_DEVICES=0 python3 main.py \
    --do_predict \
    --validation_file $validation_file \
    --test_file $test_file \
    --prompt_column content \
    --response_column summary \
    --model_name_or_path $model_name_or_path \
    --ptuning_checkpoint $ptuning_checkpoint \
    --output_dir $output_dir \
    --overwrite_output_dir \
    --max_source_length 64 \
    --max_target_length 64 \
    --per_device_eval_batch_size 1 \
    --predict_with_generate \
    --pre_seq_len $PRE_SEQ_LEN \
    --quantization_bit 4
    # --overwrite_cache \
