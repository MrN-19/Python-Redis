import socket

class SocketClient:

    def __init__(self,host:str = "127.0.0.1",port:int = 6379) -> None:

        self.__host:str = host
        self.__port:int = port

        self.__socket_client:socket.socket = socket.socket()

    def connect(self):
        
        try:
            self.__socket_client.connect((self.__host,self.__port))
        except:
            print("Failed to Connect (%s,%s)" % self.__host % str(self.__port))


    def send(self,text_data:str) -> None:

        self.__socket_client.send(text_data.encode("utf-8"))

    def receive(self) -> str:

        return self.__socket_client.recv(1024).decode("utf-8")
    
    def close(self) -> None:

        self.__socket_client.close()