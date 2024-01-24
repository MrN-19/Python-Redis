import sys
from src.client import SocketClient


socket_client = SocketClient()

print("Socket Started")

socket_client.connect()


while True:
    command:str = input("redis 127.0.0.1:6379 > ")

    if command == "exit":
        sys.exit(0)

    socket_client.send(command)

    print(socket_client.receive())