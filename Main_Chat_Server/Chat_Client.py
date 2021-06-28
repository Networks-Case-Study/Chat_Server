import socket
import threading


# Sending the msg to the server
def send(uname):
    while True:
        msg = input(f'\n{uname} > ')
        data = uname + '>>' + msg
        cli_sock.send(data.encode())


# Recieving the broadcast msg from the server
def receive():
    while True:
        data = cli_sock.recv(1024)
        print('\n\t' + str(data.decode()))


if __name__ == "__main__":
    # Creating a socket
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to the socket
    HOST = 'localhost'
    PORT = 6000
    cli_sock.connect((HOST, PORT))

    uname = input('Enter your name to enter the chat > ')
    if uname == 'C_Op':
        print('Connected to host as a Channel Operator...')
    else:
        print('Connected to remote host...')

    thread_send = threading.Thread(target=send, args=[uname])
    thread_send.start()

    thread_receive = threading.Thread(target=receive)
    thread_receive.start()
