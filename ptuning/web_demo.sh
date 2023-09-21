source ptuning_config.sh

CUDA_VISIBLE_DEVICES=0 python3 web_demo.py \
    --model_name_or_path $model_name_or_path \
    --pre_seq_len $PRE_SEQ_LEN
    # --ptuning_checkpoint $ptuning_checkpoint \

