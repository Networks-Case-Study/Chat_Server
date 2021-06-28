from common import Client


def runClient():
    print("Welcome to Client...")
    winsize = int(input("Enter a window size: "))
    client = Client(1, 10000, 10, winsize, '[CLIENT]:')
    client.runClientNode('hello.txt')


if __name__ == '__main__':
    runClient()
