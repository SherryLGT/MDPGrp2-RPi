import socket
import time


class TCPServer():
    def __init__(self, ip, port, buffer_size=1024):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(1)  # maximum backlog of connections
        print("[TCPServer] - Listening on {}:{}".format(self.ip, self.port))

    def accept(self):
        self.client_conn, client_addr = self.server_socket.accept()
        self.connected = True
        print("[TCPServer] - Accepted connection from {}:{}".format(client_addr[0],
                                                                    client_addr[1]))  # ip:port

    def recv(self):
        try:
            data = self.client_conn.recv(self.buffer_size)
        except:
            return None
        if not data:
            return None
        data_text = data.decode('utf-8')
        print("[TCPServer] - Receieved data: {}".format(data_text))
        return data_text

    def send(self, data):
        try:
            self.client_conn.send(data.encode('utf-8'))
            print("[TCPServer] - Sent data: {}".format(data))
        except:
            print("[TCPServer] - Error sending data: {}".format(data))

    def close_client(self):
        try:
            self.client_conn.close()
            self.connected = False
            print("[TCPServer] - Client disconnected")
        except:
            pass

    def close_server(self):
        try:
            self.server_socket.close()
            print("[TCPServer] - Server closed")
        except:
            pass
