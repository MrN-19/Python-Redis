

from typing import Dict,Any


class RedisDatabase:

    def __init__(self) -> None:
        self.db:Dict[str,Any] = {}

    def __setitem__(self,key:str,value:Any) -> None:
        
        self.db[key] = value

    def __getitem__(self,key:str) -> Any:

        if key in self.db.keys():

            return self.db[key]
            
        raise KeyError("Key Not Found")
    
    def get(self,key:Any,default:Any) -> Any:

        try:
            return self.db[key]
        except KeyError:
            return default

    def remove_key(self,key:str) -> None:

        if self.exists(key):
            del self.db[key]

    def exists(self,key:str) -> bool:

        return bool(self.db.get(key) is not None)
    
    def keys(self):
        return self.db.keys()
    
    