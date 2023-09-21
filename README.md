# Model-SL-Personality-Experiment Documentation

This guide provides a brief overview of the Model-SL-Personality-Experiment for developers.

## Setup
### Prerequisites

1. **Checkpoints**: Download official checkpoints and place them in the `chatglm_6b` folder.
2. **Datasets**: Acquire necessary datasets and move them to the `data` folder.

### Execution

1. Navigate to the `ptuning` directory: `cd ptuning`
2. To adjust training and evaluation configurations, edit the `pthning_config.sh` file.
3. Run the training script: 
    ```bash
    bash train.sh
    ```
4. Post-training, run the evaluation: 
    ```bash
    bash evaluate.sh
    ```

### Web Demo

For inference and to view the results of your training, execute: 
```
bash web_demo.sh
```

## Model Modifications

### Modeling Changes
In `modeling_chatglm.py`, the `IdentityMappingModule` provides functionalities related to identity mappings in the model. You can change its location or behavior according to your requirements.

### Freezing Utilities
The files `utility.py` and `trainer.py` are equipped with the necessary tools and methods to handle freezing operations on the model. If you need to make any adjustments or implement additional functionalities related to model freezing, these are the go-to files.

## Navigating the Codebase

- **TODO Labels**: Look for the `TODO` labels within the code. These markers indicate segments where further action or enhancement is anticipated but hasn't been addressed yet.

- **FIXME Labels**: Search for `FIXME` labels. These highlight sections of the code that have known issues or anomalies requiring fixes.

## Contribution

Before pushing any modifications, ensure thorough testing to guarantee the stability and efficiency of the Model-SL-Personality-Experiment.

---

For a swift codebase traversal, use tools like `grep` or your IDE's search functionality. Searching for the `TODO` and `FIXME` labels will quickly lead you to the sections needing attention.