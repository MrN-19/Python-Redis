import sys
import socket
from typing import Callable

from .database import RedisDatabase

class SocketConnection:

    def __init__(self,redis_database:RedisDatabase,ip:str = "127.0.0.1",port:int = 6379):

        self.__ip:str = ip
        self.__port:int = port

        self.__redis_database:RedisDatabase = redis_database

    @property
    def ip(self) -> str:return self.__ip

    @property
    def port(self) -> int:return self.__port

    def start(self,action:Callable,*args,**kwargs):

        


        print(f"Server is Listening On {self.ip} : {self.port}")

        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as socket_server:

            socket_server.bind((self.__ip,self.__port))
            socket_server.listen()

            client,address = socket_server.accept()    

            while True:
                data:str = client.recv(2048).decode("utf-8")

                print(f"{data} From {address}")

                if data == "exit":
                    sys.exit(0)

                response:str = action(command = data,db = self.__redis_database,*args,**kwargs)

                if response is None:
                    client.send("Command Not Found ...".encode("utf-8"))
                else:
                    client.send(response.encode("utf-8"))