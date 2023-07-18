import socket
from typing import Any

from helper import NoneException

from helper import IN_QUEUE, OUT_QUEUE, CONDITION

class SplitSocket:
    def __init__(self, host: str, port: int):
        # Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host, port)
        print(f"Starting server on {host}:{port}")
        try:
            self.server_socket.bind(server_address)
            # Listen for incoming connections
            self.server_socket.listen(1)
            print('recv: waiting for a connection')
            self.client_socket, client_address = self.server_socket.accept()
            print('client connected:', client_address)
        except Exception as e:
            print(f"Could not start server: {e}")

    def receive_data(self) -> Any:
        """
        Receives data and pushes it into the data_queue.
        """
        CONDITION.acquire()

        data = self._receive_data()
        print(f"[SERVER]: Received data.")

        data = {"byte_data": data}
        IN_QUEUE.put(data)
        CONDITION.notify()

        CONDITION.wait()
        data = OUT_QUEUE.get()
        self._send_data(data["byte_data"])

        print(f"[SERVER]: Send data back.")
        # CONDITION.release()

    def _send_data(self, data: bytes):
        """Sends raw data through the socket."""
        try:
            self.client_socket.sendall(data + b"EOF")
            # print(str(len(data)/4096))
        except Exception as e:
            print(f"Error sending data: {e}")

    def _receive_data(self) -> bytes:

        """Receives raw data from the socket."""
        data = []
        # try:
        while True:
            chunk = self.client_socket.recv(4096)
            if b"EOF" in chunk:
                data.append(chunk[:-3])
                break  # no more data
            # print(repr(chunk))
            data.append(chunk)
        # print("recvd data !!! " + str(len(data)))
        data = b"".join(data)
        if data == b"":
            raise NoneException("None received")
        return data
        # except Exception as e:
        #     print(f"Error receiving data: {e}")

    def run(self) -> None:
        """
        Runs the Flask server.
        """
        while True:
            self.receive_data()

    def close_connection(self):
        if self.client_socket:
            self.client_socket.close()
