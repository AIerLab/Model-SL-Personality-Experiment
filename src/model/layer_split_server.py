import pickle
from time import sleep

import torch
from model import AbstractModel
from queue import Queue

from helper import IN_QUEUE, OUT_QUEUE, CONDITION


class SplitServerLayer(AbstractModel):
    def __init__(self, model_dir: str, device=None, first_layer=False, last_layer=False):
        super().__init__(model_dir)
        # get all model layers
        self.first_layer = first_layer
        self.last_layer = last_layer

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        CONDITION.acquire()
        device = x.device

        if not self.first_layer:
            # pickle the tensor data
            serialized_data = pickle.dumps(x)
            # Send the result to the server
            data = {"byte_data": serialized_data, "stage": "forward"}
            OUT_QUEUE.put(data)
            CONDITION.notify()
            print("[LAYER]: Send intermediate result back.")

        CONDITION.wait()
        data = IN_QUEUE.get()
        print("[LAYER]: Receive intermediate result.")
        # print(repr(serialized_data))
        x = pickle.loads(data["byte_data"])

        if type(x) is str:
            CONDITION.wait()
            data = IN_QUEUE.get()
            # print(repr(serialized_data))
            x = pickle.loads(data["byte_data"])
            x.to(device)
        CONDITION.release()
        return x

    def backward(self, grad: torch.Tensor):
        if not self.last_layer:
            while not self.out_queue.empty():
                pass
            # pickle the tensor data
            serialized_data = pickle.dumps(grad)
            # Send the result to the server
            data = {"byte_data": serialized_data, "stage": "backward"}
            self.out_queue.put(data) # FIXME

        while self.in_queue.empty():
            pass
        data = self.in_queue.get()
        # print(repr(serialized_data))
        grad = pickle.loads(data["byte_data"])
        grad = grad.to(self.device)

        return grad
