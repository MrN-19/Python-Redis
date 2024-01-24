

class RedisException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class RedisKeyException(RedisException):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class RedisValueExcpetion(RedisException):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)