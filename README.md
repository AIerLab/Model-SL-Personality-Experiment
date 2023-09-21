# Model-SL-Personality-Experiment Documentation

This guide provides a brief overview of the Model-SL-Personality-Experiment for developers.

## Setup
### Prerequisites

1. **Checkpoints**: Download official checkpoints and place them in the `chatglm_6b` folder.
2. **Datasets**: Acquire necessary datasets and move them to the `data` folder.

### Execution

1. Navigate to the `ptuning` directory: `cd ptuning`
2. Edit the `train.sh` and `evaluate.sh` script as needed.
3. Run the training script: `bash train.sh`
4. Post-training, run the evaluation: `bash evaluate.sh`

## Model Modifications

### `modeling_chatglm.py`
This file contains the `IdentityMappingModule`. If you wish to change the location or behavior of the module, make the necessary modifications here.

### `utility.py` & `trainer.py`
Both files provide utilities for freezing the model. If you require any changes related to model freezing, refer to these files.

## Navigating the Codebase

- **TODO Labels**: Look for the `TODO` labels within the code. These are places where some action or enhancement is needed but hasn't been completed yet.
- **FIXME Labels**: Search for `FIXME` labels. These indicate parts of the code that have known issues or bugs that need fixing.

## Contribution

Ensure you test your modifications thoroughly before committing. This will ensure the stability and efficiency of the Model-SL-Personality-Experiment.

---

Use tools like `grep` or your IDE's search function to quickly navigate to `TODO` and `FIXME` labels. These labels will assist in identifying areas of the codebase that require attention.