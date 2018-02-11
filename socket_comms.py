import bluetooth
import socket
import threading
import time
import serial

def start_tcp_server(bind_ip, bind_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((bind_ip, bind_port))
    server_socket.listen(5)  # max backlog of connections

    print("Listening on {}:{}".format(bind_ip, bind_port))

    global running
    while running:
        global tcp_client_socket
        tcp_client_socket, client_info = server_socket.accept()
        print("Accepted TCP connection from {}:{}".format(
            client_info[0], client_info[1]))  # ip:port

        try:
            while running:
                data = tcp_client_socket.recv(1024)
                if len(data) == 0:
                    tcp_client_socket.close()
                    print("TCP disconnected")
                    break
                global bt_client_socket
                try:
                    bt_client_socket.send(data)
                except:
                    print("Bluetooth sending error")
        except:
            tcp_client_socket.close()
            print("TCP disconnected")

    server_socket.close()
    print("TCP server stopped")


def start_bt_server(channel):
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", channel))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    bluetooth.advertise_service(server_sock, "MDPGrp2-BTServer",
                                service_id=uuid,
                                service_classes=[
                                    uuid, bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                # protocols = [ OBEX_UUID ]
                                )

    print("Waiting for connection on RFCOMM channel %d" % port)

    global running
    while running:
        global bt_client_socket
        bt_client_socket, client_info = server_sock.accept()
        print("Accepted Bluetooth connection from {}:{}".format(
            client_info[0], client_info[1]))

        try:
            while running:
                data = bt_client_socket.recv(1024)
                if len(data) == 0:
                    bt_client_socket.close()
                    print("Bluetooth disconnected")
                    break
                global tcp_client_socket
                try:
                    tcp_client_socket.send(data)
                except:
                    print("TCP sending error")
        except IOError:
            bt_client_socket.close()
            print("Bluetooth disconnected")

    server_sock.close()
    print("Bluetooth server stopped")


if __name__ == "__main__":
    global running
    running = True
    t1 = threading.Thread(target=start_bt_server, args=(
        10,))  # channel 4 | 10 for testing
    t1.start()
    t2 = threading.Thread(target=start_tcp_server, args=(
        "0.0.0.0", 69))  # 192.168.2.1 | 10.42.0.102
    t2.start()
    try:
        time.sleep(1)
        raw_input("Press enter to quit \n")
        running = False
    except KeyboardInterrupt:
        running = False
    t1.join()
    t2.join()
