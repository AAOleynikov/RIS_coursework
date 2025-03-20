import json

from flask import current_app
from redis import Redis, DataError


class RedisCache:
    def __init__(self, config: dict):
        self.config = config
        self.conn = self._connect()

    def _connect(self):
        conn = Redis(**self.config)
        return conn

    def set_value(self, name: str, value_dict: dict, ttl: float):
        value_js = json.dumps(value_dict)
        try:
            self.conn.set(name=name, value=value_js)
            if ttl > 0:
                self.conn.expire(name, ttl)
                return True
        except DataError as err:
            current_app.logger.error(f'Ошибка при сохранении данных в кэш "{name}": {err}')
            return False

    def get_value(self, name):
        try:
            value_js = self.conn.get(name)
            if value_js:
                value_dict = json.loads(value_js)
                return value_dict
            else:
                return None
        except DataError as err:
            current_app.logger.error(f'Ошибка при получении данных из кэша "{name}": {err}')
            return False
