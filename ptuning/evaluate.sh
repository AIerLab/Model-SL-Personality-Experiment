PRE_SEQ_LEN=128
LR=2e-2
STEP=500
CHECKPOINT=chatglm-6b-pt-$PRE_SEQ_LEN-$LR-0

validation_file=../data/dev.json
test_file=../data/dev.json
model_name_or_path=../chatglm_6b

model_checkpoint_path=../output/$CHECKPOINT/checkpoint-$STEP # suppose to be a different path from the output one.
output_dir=../output/$CHECKPOINT

CUDA_VISIBLE_DEVICES=0 python3 main.py \
    --do_predict \
    --validation_file $validation_file \
    --test_file $test_file \
    --prompt_column content \
    --response_column summary \
    --model_name_or_path $model_name_or_path \
    --ptuning_checkpoint $model_checkpoint_path \
    --output_dir $output_dir \
    --overwrite_output_dir \
    --max_source_length 64 \
    --max_target_length 64 \
    --per_device_eval_batch_size 1 \
    --predict_with_generate \
    --pre_seq_len $PRE_SEQ_LEN \
    --quantization_bit 4
    # --overwrite_cache \
