from src.server import SocketConnection
from src.server.command_handler import CommandManager
from src.server.database import RedisDatabase

redis_database = RedisDatabase()

socket = SocketConnection(redis_database)

command_manager = CommandManager()

socket.start(command_manager)




