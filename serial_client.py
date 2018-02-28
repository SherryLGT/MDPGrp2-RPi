import serial
import time


class SerialClient():
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate

    def connect(self):
        try:
            self.client_conn = serial.Serial(
                self.port, self.baud_rate, timeout=None)
            print(
                "[SerialClient] - Connection on {}:{}".format(self.port, self.baud_rate))
            return True
        except:
            time.sleep(1)
            return False

    def recv(self):
        try:
            data = self.client_conn.readline()
        except:
            return None
        if not data:
            return None
        data_text = data.decode('utf-8')
        print("[SerialClient] - Receieved data: {}".format(data_text))
        return data_text

    def send(self, data):
        try:
            self.client_conn.send((data+"\n").encode('utf-8'))
            print("[SerialClient] - Sent data: {}".format(data))
        except:
            print("[SerialClient] - Error sending data: {}".format(data))

    def close_conn(self):
        try:
            self.client_conn.close()
            print("[SerialClient] - Disconnected")
        except:
            pass
