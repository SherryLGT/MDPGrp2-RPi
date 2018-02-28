import threading
import time
import Queue

from tcp_server import TCPServer
from bt_server import BTServer
from serial_client import SerialClient


def run_tcp_server(ip, port, android_queue, arduino_queue):
    global running
    global pc_conn
    pc_conn = TCPServer(ip, port)
    pc_conn.run()
    while running:
        pc_conn.accept()
        while running:
            data = pc_conn.recv()
            if data is None:
                break
            if data[0] == "#":  # change to decided message
                android_queue.put(data)
            else:
                arduino_queue.put(data)
        pc_conn.close_client()
    pc_conn.close_server()


def run_bt_server(channel, pc_queue, arduino_queue):
    global running
    global android_conn
    android_conn = BTServer(channel)
    android_conn.run()
    while running:
        android_conn.accept()
        while running:
            data = android_conn.recv()
            if data is None:
                break
            if data[0] == "#":  # change to decided message
                pc_queue.put(data)
            else:
                arduino_queue.put(data)
        android_conn.close_client()
    android_conn.close_server()


def run_serial_client(port, baud_rate, pc_queue):
    global running
    global arduino_conn
    arduino_conn = SerialClient(port, baud_rate)
    while running:
        connected = False
        while not connected and running:
            connected = arduino_conn.connect()
        while running:
            data = arduino_conn.recv()
            if data is None:
                break
            pc_queue.put(data)
        arduino_conn.close_conn()


def send_tcp_server(pc_queue):
    global running
    global pc_conn
    while running:
        if not pc_queue.empty():
            pc_conn.send(pc_queue.get())


def send_bt_server(android_queue):
    global running
    global android_conn
    while running:
        if not android_queue.empty():
            android_conn.send(android_queue.get())


def send_serial_client(arduino_queue):
    global running
    global arduino_conn
    while running:
        if not arduino_queue.empty():
            arduino_conn.send(arduino_queue.get())


if __name__ == "__main__":
    global running
    running = True
    pc_queue = Queue.Queue()
    android_queue = Queue.Queue()
    arduino_queue = Queue.Queue()
    t1 = threading.Thread(target=run_bt_server, args=(10, pc_queue, arduino_queue)
                          )  # channel 4 | 10 for testing
    t2 = threading.Thread(target=run_tcp_server,
                          args=("0.0.0.0", 99, android_queue, arduino_queue))  # 192.168.2.1
    t3 = threading.Thread(target=run_serial_client,
                          args=("/dev/ttyACM0", 9600, pc_queue))
    t4 = threading.Thread(target=send_bt_server, args=(android_queue,))
    t5 = threading.Thread(target=send_tcp_server, args=(pc_queue,))
    t6 = threading.Thread(target=send_serial_client, args=(arduino_queue,))
    t1.start()  # bluetooth server listening thread
    t2.start()  # tcp server listening thread
    t3.start()  # serial client listening thread
    t4.start()  # bluetooth server sending thread
    t5.start()  # tcp server sending thread
    t6.start()  # serial client sending thread

    try:
        time.sleep(1)
        raw_input("Press Enter to quit. \n")
        running = False
    except KeyboardInterrupt:
        running = False

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
