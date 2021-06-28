from common import Server


def runServer():
    print("Welcome to Server")
    winsize = int(input("Enter a window size: "))
    server = Server(1, 10001, 1000, winsize, '[SERVER]:')
    server.runServerNode()


if __name__ == '__main__':
    runServer()
