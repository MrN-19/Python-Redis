from typing import Iterable,Any,Collection,List,Tuple
from datetime import datetime

from .exceptions import RedisKeyException,RedisValueExcpetion
from .database import RedisDatabase

class CommandManager:

    def __init__(self) -> None:
        ...

    def __call__(self,*args,**kwargs) -> None:

        self.__command:str = kwargs.get("command")
        self.__db:RedisDatabase = kwargs.get("db")

        return self.start()

    @property
    def command(self) -> str:return self.__command

    def start(self) -> Any:

        extracted_command:Iterable[str] = self.extract_commands()

        return self.check_first_part_of_command(extracted_command)

    def extract_commands(self) -> list[str]:

        command_extracted = self.command.split(" ")

        return command_extracted
    
    def check_first_part_of_command(self,command_extracted:list[str]) -> Any:

        first:str = command_extracted[0]

        first = first.lower()

        if first in StringCommandHandler.REDIS_STRING_COMMANDS:
            
            return StringCommandHandler(command_extracted,self.__db).check_command()

            # pass data to StringChecker Class

        elif first.startswith("ping"):

            if self.__db:
                return "PONG"
            
        elif first.startswith("h"):
            # hash commands
            ...

class StringCommandHandler:

    REDIS_STRING_COMMANDS:Collection[str] = (
        "set","get","setex","setnx","getrange","getset","mget","strlen","mset"
    )

    NIL:str = "(nil)"
    OK:str = "OK"
    INTEGER0 = "integer (0)"

    def __init__(self,command:Iterable[str],database_instance:RedisDatabase) -> None:

        self.__command:Iterable[str] = command
        
        self.__db:RedisDatabase = database_instance

    @property
    def command(self) -> Iterable[str]:return self.__command


    def check_command(self) -> Any:

        first_part_command:str = self.command[0]

        match first_part_command:

            case "set":

                key:str
                value:str

                try:
                    key:str = self.command[1]
                    value = self.command[2]

                except IndexError:
                    return self.__argument_error("set") # we should return it instead of raise error
                
                self.__db[key] = (str(value),None,None)

                return self.OK
            
            case "setex": # Set Value by Expire time
                # set expire

                key:str
                seconds:int
                value:str

                try:

                    key = self.command[1]
                    seconds = self.command[2]
                    value = self.command[3]

                    self.__db[key] = (str(value),datetime.now(),int(seconds))

                    # not finished yet
                    return self.OK

                except IndexError:
                    return self.__argument_error("setex")

            case "setnx": # Set Not Exists

                key:str
                value:str

                try:

                    key = self.__get_key()
                    value = self.__get_value()

                    if not (key in self.__db.keys()):

                        self.__db[key] = (str(value),None,None)
                        return self.OK
                    
                    return self.INTEGER0

                except IndexError:
                    return self.__argument_error("setnx")

        
            case "get": # we have warning about number of argument in this section

                key:str
                
                try:

                    key = self.__get_key()

                    if self.__db.exists(key):

                        if self.__check_time_exists(key):

                            if self.__check_expire_time(key):
                                return self.__db[key][0]
                            
                            self.__db.remove_key(key)
                            return self.NIL
                        
                        
                        return "%s" % self.__db[key][0]
                
                except KeyError:
                    return self.NIL
                
                except IndexError:
                    return self.__argument_error("get")
            
            case "getrange":

                key:str
                value:str
                start:int
                end:int

                try:
                    key = self.command[1]

                    if self.__db.exists(key):

                        start = int(self.command[2])
                        end = int(self.command[3])

                        value = self.__get_value()

                        if (start >= end):
                            return ""

                        if self.__check_time_exists(key):

                            if self.__check_expire_time(key):

                                if (end + 1 > len(value)):
                                    return value

                                return value[start:end + 1]
                            self.__db.remove_key(key)
                            return self.NIL

                        if (end + 1 > len(value)):
                            return value
                        
                        return value[start:end + 1]
                    
                    return self.NIL

                except IndexError:
                    
                    return self.__argument_error("getrange")
                except ValueError:
                    
                    return self.__argument_error("getrange")

            case "getset":

                key:str
                value:str

                try:
                    key = self.command[1]
                    value = self.command[2]

                    last_value = self.__db[key][0]

                    self.__db[key] = (str(value),None,None)

                    return last_value

                except IndexError:
                    return self.__argument_error("getset")
                
                except KeyError:
                    return self.NIL
                
            case "mget":

                keys:Collection[str]

                try:

                    keys = list(self.command[1:])

                    values:List[str] = []

                    for key in keys:
                        
                        if self.__db.exists(key):

                            values.append(self.__db[key][0])
                        else:
                            values.append(self.NIL)

                    return "\n".join(values)

                except KeyError:
                    return self.NIL
            
            case "strlen":
                
                try:

                    key:str = self.__get_key()

                    if self.__check_time_exists(key):

                        if self.__check_expire_time(key):
                            
                            return str(len(self.__db[key][0]))

                        return "0"

                    return str(len(self.__db[key][0]))

                except IndexError:
                    return self.__argument_error("strlen")
                
                except KeyError:

                    return self.NIL
                
            case "mset":

                try:
                    

                    if len(self.command[1:]) % 2 != 0:
                        return self.__argument_error("mset")

                    index:int = 1
                    while index < len(self.command):

                        try:
                            self.__db[self.command[index]] = (self.command[index + 1],None,None)
                            index += 2
                        
                        except IndexError:
                            break 

                    return self.OK

                except IndexError:
                    return self.__argument_error("mset")
    
    def __get_key(self) -> str:
        return self.command[1]
    
    def __get_value(self) -> str:
        return self.command[2]
    
    def __check_expire_time(self,key:str) -> bool:
        
        if (datetime.now() - self.__db[key][1]).seconds < self.__db[key][2]:
            return True
        
        return False
    
    def __check_time_exists(self,key:str) -> bool:
        
        return (self.__db[key][1] is not None) or (self.__db[key][2] is not None)
    
    def __argument_error(self,command_name:str) -> str:
        return f"(error) ERR wrong number of arguments for \'{command_name}'\ command"
    
    def __key_exists(self,key:str) -> str | None:

        if not self.__db.exists(key):
            return self.NIL
        

    def __multi_set(self):
        ...
        

        