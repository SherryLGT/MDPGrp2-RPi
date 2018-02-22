import threading
import Queue
import serial
import time

from arduino_test import*

class Multithread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        # initialize interfaces
        self.arduino_interface = ArduinoInterface()

        # create connections
        self.arduino_interface.connect()

        # create queues
        self.toandroid_queue = Queue.Queue(maxsize=0)
        self.toalgo_queue = Queue.Queue(maxsize=0)
        self.toarduino_queue = Queue.Queue(maxsize=0)
        # test
        self.toarduino_queue.put_nowait("")
        self.toarduino_queue.put_nowait("hello1")
        self.toarduino_queue.put_nowait("hello2")
        self.toarduino_queue.put_nowait("hello3")

        time.sleep(1)

    # arduino methods
    def sendto_serial(self, arduino_q):
        while True:
            if not arduino_q.empty():
                msg = arduino_q.get_nowait()
                if len(msg):
                    self.arduino_interface.senddata(msg)
                    print("[sendto_serial] " + msg)
                time.sleep(0.6)                               # impt! if remove, arduino wont receive

    def recvfrom_serial(self, algo_q, android_q):
        # while True:
        #     msg = self.arduino_interface.recvdata()
        #     if msg is not None:
        #         if msg:
        #             if (msg[:2] == 'AN'):                   # first two letters is AN - android
        #                 android_q.put_nowait(msg[3:])       # put the rest of the msg into android_q, starting from 3rd char
        #                 print("[recvfrom_serial] From AN: " + msg)
        #             elif (msg[:2] == 'AL'):                  # first two letters is AL - algo
        #                 algo_q.put_nowait(msg[3:])
        #                 print("[recvfrom_serial] From AL: " + msg)
        #             else:                                   # unknown msg
        #                 print("[recvfrom_serial] " + msg)
        #         else:
        #             print("msg is empty")
        #     else:
        #         print("msg is null")
        while True:
            msg = self.arduino_interface.recvdata()
            if len(msg):
                print("[recvfrom_serial] %s" % msg)
                # print("queue: %d" % self.toarduino_queue.qsize())

    # # android methods
    # def sendto_bluetooth(self, android_q):
    #     while True:
    #         if not android_q.empty():
    #             msg = android_q.get_nowait()
    #             self.android_thread.#call send method

    # def recvfrom_bluetooth(self, algo_q, arduino_q):
    #     while True:
    # 

    # # algo methods
    # def sendto_tcp(self, algo_q):
    #     while True:
    #         if not algo_q.empty():
    #             msg = algo_q.get_nowait()
    #             self.algo_thread.#call send method

    # def recvfrom_tcp(self, android_q, arduino_q):
    #     while True:
    # 

    def create_threads(self):
        serial_read = threading.Thread(target = self.recvfrom_serial, args=(self.toalgo_queue, self.toandroid_queue,))
        serial_write = threading.Thread(target = self.sendto_serial, args=(self.toarduino_queue,))
        # bluetooth_read = threading.Thread(target = self.recvfrom_bluetooth, args=(self.toalgo_queue, self.toarduino_queue,))
        # bluetooth_write = threading.Thread(target = self.sendto_bluetooth, args=(self.toandroid_queue,))
        # tcp_read = threading.Thread(target = self.recvfrom_tcp, args=(self.toandroid_queue, self.toarduino_queue,))
        # tcp_write = threading.Thread(target = self.sendto_tcp, args=(self.toalgo_queue,))

        serial_read.daemon = True
        serial_write.daemon = True
        # bluetooth_read.daemon = True
        # bluetooth_write.daemon = True
        # tcp_read.daemon = True
        # tcp_write.daemon = True

        serial_read.start()
        serial_write.start()
        # bluetooth_read.start()
        # bluetooth_write.start()
        # tcp_read.start()
        # tcp_write.start()

    def keepmain_alive(self):
        while True:
            time.sleep(1)

    def close_allsockets(self):
        self.arduino_interface.disconnect()

if __name__ == "__main__":
    rpi_server = Multithread()
    try:
        rpi_server.create_threads()
        rpi_server.keepmain_alive()
    except KeyboardInterrupt:
        rpi_server.close_allsockets()
        print("Closed all sockets")
        # close sockets - serial, bluetooth and tcp