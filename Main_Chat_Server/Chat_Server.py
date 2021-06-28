import socket
import threading


def accept_client():
    while True:
        cli_sock, cli_add = ser_sock.accept()
        CONNECTION_LIST.append(cli_sock)
        thread_client = threading.Thread(
            target=msgrecieve_usr, args=[cli_sock])
        thread_client.start()


def msgrecieve_usr(cli_sock):                                       # Recieving the msg
    while True:
        try:
            data = cli_sock.recv(1024)
            if data:
                name = data.decode()
                uname = name.split('>>')[0]
                if uname == 'C_Op':
                    msg = 'Channel Admin'+'>>'+name.split('>>')[1]
                    b_usrs(cli_sock, msg)
                else:
                    m_usr(cli_sock, data)
        except Exception as x:
            print(x)
            break


# Printing the msg sent by the user
def m_usr(cs_sock, msg):
    for client in CONNECTION_LIST:
        if client == cs_sock:
            print(msg.decode())


# Broadcasting the msg sent by the admin
def b_usrs(cs_sock, msg):
    for client in CONNECTION_LIST:
        if client != cs_sock:
            client.send(msg.encode())


if __name__ == "__main__":
    CONNECTION_LIST = []
    ser_sock = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)   # Creating a socket

    # Binding a socket
    HOST = 'localhost'
    PORT = 6000
    ser_sock.bind((HOST, PORT))

    ser_sock.listen(1)
    print('Chat server started on port : ' + str(PORT))

    thread_ac = threading.Thread(target=accept_client)
    thread_ac.start()
