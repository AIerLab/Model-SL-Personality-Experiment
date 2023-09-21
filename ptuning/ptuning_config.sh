PRE_SEQ_LEN=128
LR=2e-2
STEP=500
CHECKPOINT=chatglm-6b-pt-$PRE_SEQ_LEN-$LR-0

train_file=../data/train.json
validation_file=../data/dev.json
test_file=../data/dev.json
model_name_or_path=../chatglm_6b

ptuning_checkpoint=../output/$CHECKPOINT/checkpoint-$STEP # suppose to be a different path from the output one.
output_dir=../output/$CHECKPOINT