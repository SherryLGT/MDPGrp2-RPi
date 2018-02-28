import bluetooth
import time


class BTServer():
    def __init__(self, channel, buffer_size=1024):
        self.channel = channel
        self.buffer_size = buffer_size
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def run(self):
        self.server_socket.bind(("", self.channel))
        self.server_socket.listen(1)
        port = self.server_socket.getsockname()[1]
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        bluetooth.advertise_service(self.server_socket, "MDPGrp2-BTServer",
                                    service_id=uuid,
                                    service_classes=[
                                        uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                    # protocols = [ OBEX_UUID ]
                                    )
        print("[BTServer] - Waiting for connection on RFCOMM channel {}".format(port))

    def accept(self):
        self.client_conn, client_addr = self.server_socket.accept()
        self.connected = True
        print("[BTServer] - Accepted connection from {}:{}".format(client_addr[0],
                                                                   client_addr[1]))  # ip:port

    def recv(self):
        try:
            data = self.client_conn.recv(self.buffer_size)
        except:
            return None
        if len(data) == 0:
            return None
        data_text = data.decode('utf-8')
        print("[BTServer] - Receieved data: {}".format(data_text))
        return data_text

    def send(self, data):
        try:
            self.client_conn.send((data+"\n").encode('utf-8'))
            print("[BTServer] - Sent data: {}".format(data))
        except:
            print("[BTServer] - Error sending data: {}".format(data))

    def close_client(self):
        try:
            self.client_conn.close()
            self.connected = False
            print("[BTServer] - Client disconnected")
        except:
            pass

    def close_server(self):
        try:
            self.server_socket.close()
            print("[BTServer] - Server closed")
        except:
            pass
