from functools import wraps

from flask import current_app

from cache.redis_cache import RedisCache


def fetch_from_cache(cache_name: str, cache_config: dict):
    cache_conn = RedisCache(cache_config['redis'])
    ttl = cache_config['ttl']

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                cached_value = cache_conn.get_value(cache_name)
                if cached_value:
                    current_app.logger.info(f'Данные из кэша "{cache_name}" были извлечены успешно')
                    return cached_value
                current_app.logger.info(f'Данные из кэша "{cache_name}" отсутствуют')
            except Exception as e:
                current_app.logger.error(f'Ошибка при извлечении из кэша "{cache_name}": {e}')

            current_app.logger.debug(f'Обращение к базе данных за незакэшированными данными')
            result = f(*args, **kwargs)

            try:
                cache_conn.set_value(cache_name, result, ttl)
                current_app.logger.info(f'Данные были успешно сохранены в кэш "{cache_name}"')
            except Exception as e:
                current_app.logger.error(f'Ошибка при сохранении в кэш "{cache_name}" данных из базы данных: {e}')

            return result

        return wrapper

    return decorator
