import json
import os
import pickle
from asyncio import sleep
from queue import Queue

import torch
from tqdm import tqdm

from model.chatglm_6b_split_server import ChatGLMTokenizer, ChatGLMConfig, ChatGLMForConditionalGeneration

from helper import IN_QUEUE, OUT_QUEUE, CONDITION

tokenizer_config_path = os.path.join('model', 'chatglm_6b_split_server', 'tokenizer_config.json')
model_config_path = os.path.join('model', 'chatglm_6b_split_server', 'config.json')
token_text_path = os.path.join("..", "tmp", "server", "ice_text.model")
model_state_dict_file_num = 8

class SplitServerModel:
    def __init__(self, model_dir: str = None):  # FIXME FOR TEST USE ONLY, can not be none
        if model_dir:  # FIXME FOR TEST USE ONLY, never load from server path
            model_dir = os.path.join("..", "tmp", "server")

        # Open and load the JSON file into a Python dict
        print(tokenizer_config_path)
        with open(tokenizer_config_path) as config_file:
            config_dict = json.load(config_file)

        self.tokenizer = ChatGLMTokenizer(token_text_path, **config_dict)
        # self.model = AutoModel.from_pretrained("THUDM/chatglm_6b_demo", trust_remote_code=True).half().cuda()

        # Open and load the JSON file into a Python dict
        with open(model_config_path) as config_file:
            config_dict = json.load(config_file)

        configuration = ChatGLMConfig(**config_dict)
        model = ChatGLMForConditionalGeneration(configuration, model_dir)

        # Empty dict to accumulate the state dicts from all files
        state_dict_all = {}

        # Loop over files
        for i in tqdm(range(1, model_state_dict_file_num + 1)):
            filename = f"pytorch_model-{str(i).zfill(5)}-of-{str(model_state_dict_file_num).zfill(5)}.bin"

            filepath = os.path.join(model_dir, filename)  # replace with the directory of the files
            state_dict = torch.load(filepath)
            state_dict_all.update(state_dict)

        # Load the combined state_dict into the model
        model.load_state_dict(state_dict_all, strict=False)

        self.model = model.half().cuda()

        # print(self.model)
        self.model = self.model.eval()
        self.history = []
        self.count = 0

    def build_prompt(self) -> str:
        # prompt = "Welcome to the ChatGLM-6B model. Type your message."
        prompt = ""
        if self.history:
            _, response = self.history[-1]
            prompt += response
        return prompt

    def process(self) -> str:
        CONDITION.acquire()
        CONDITION.wait()
        print("[MODEL]: Input query received")
        data = IN_QUEUE.get()
        # print(repr(serialized_data))
        query = pickle.loads(data["byte_data"])

        for response, self.history in self.model.stream_chat(self.tokenizer, query, history=self.history):
            if self.count == 1000:  # TODO hard coded
                self.count = 0
                self.history = []
            self.count += 1

            print(f"[HISTORY]: {response}")

            print("[MODEL]: Sending current result back")
            # pickle the tensor data
            serialized_data = pickle.dumps(response)
            # Send the result to the server
            data = {"byte_data": serialized_data, "stage": "forward"}
            OUT_QUEUE.put(data)
            CONDITION.notify()

            # Waiting to start next iter
            CONDITION.wait()
            IN_QUEUE.get()

        print("[MODEL]: Sending None as ending.")
        # pickle the tensor data
        serialized_data = pickle.dumps(None)
        # Send the result to the server
        data = {"byte_data": serialized_data, "stage": "forward"}
        OUT_QUEUE.put(data)
        CONDITION.notify()

        CONDITION.release()

        return self.build_prompt()

    def clear(self) -> None:
        self.history = []

    def stop(self) -> None:
        self.model = None

