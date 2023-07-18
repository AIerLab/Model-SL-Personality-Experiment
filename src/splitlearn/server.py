"""
This script is used to define a Server class for a Flask server.
"""
import base64
import pickle

from flask import Flask, request, jsonify, abort
from queue import Queue
from threading import Thread
from typing import Callable, Any, Optional
from time import sleep

from flask_cors import CORS

from helper import IN_QUEUE, OUT_QUEUE, CONDITION

class SplitServer:
    """
    This class defines a Server that can receive, process, and send data.
    """

    def __init__(self) -> None:
        """
        Initializer for the Server class.
        """
        self.app = Flask(__name__)
        CORS(self.app)

        self.app.add_url_rule('/intermediate', 'intermediate', self.receive_data, methods=['POST'])
        self.api_key = "secret_api_key"  # In reality, this should be securely stored and not hard-coded

    def check_auth(self) -> bool:
        """
        Checks if the API key is present and correct.
        """
        return request.headers.get('X-API-Key') == self.api_key

    def receive_data(self) -> Any:
        """
        Receives data and pushes it into the data_queue.
        """
        CONDITION.acquire()

        if not self.check_auth():
            abort(401)  # Unauthorized
        data = request.json
        for key in data:
            if "byte" in key:
                data[key] = base64.b64decode(data[key].encode('utf-8'))
        print(f"[SERVER]: Received data.")

        IN_QUEUE.put(data)
        CONDITION.notify()

        CONDITION.wait()
        data = OUT_QUEUE.get()

        for key in data:
            if "byte" in key:
                data[key] = base64.b64encode(data[key]).decode('utf-8')
        print(f"[SERVER]: Send data back.")

        CONDITION.release()

        return jsonify(data)

    def run(self, host: str, port: int) -> None:
        """
        Runs the Flask server.
        """
        self.app.run(host=host, port=port)


if __name__ == '__main__':
    server = SplitServer()
    server.run("localhost", 10086)
