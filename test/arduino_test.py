import serial
import time

PORT_NAME = '/dev/ttyACM0'  # port name of the serial port, /dev/ttyACM0
BAUD_RATE = '9600'          # data rate (bits per sec) for serial data transmission, 115200 

class ArduinoInterface:

    def __init__(self):
        self.serial_port = PORT_NAME
        self.baud_rate = BAUD_RATE

    def connect(self):
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)    # timeout=1: returns immediately when the requested number of bytes are available, otherwise wait until the timeout expires and return all bytes that were received until then
            print("[Serial] Connection to Arduino Successful!")
        except serial.SerialException as e:
            print("[Serial] Connection Error: %s" % str(e))
            self.connect()

    def disconnect(self):
        if self.ser:
            self.ser.close()
            print("[Serial] Disconnection from Arduino Successful!")
        else:
            print("[Serial] Could not disconnect as Serial Connection has not been established.")

    def recvdata(self):
        data = self.ser.readline()  # read a '\n' terminated line
        return data

    def senddata(self, msg):
        try:
            self.ser.write(str(msg).encode('UTF-8'))
            # print("buffer: %d" % self.ser.in_waiting)
        except AttributeError:
            print("error sending msg to Arduino")

# if __name__ == '__main__':
#     arduinoInterface = ArduinoInterface()
#     arduinoInterface.connect()
#     # while True:
#     #     arduinoInterface.senddata("Hi from RPi")
#     #     print("[Serial] Receiving message from Arduino...")