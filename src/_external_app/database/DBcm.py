from flask import current_app
from pymysql import connect
from pymysql.err import OperationalError


class DBContextManager:
    def __init__(self, db_config: dict):
        self.conn = None
        self.cursor = None
        self.config = db_config

    def __enter__(self):
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            current_app.logger.error(f'Ошибка при работе с базой данных: {err.args[0]} : {err.args[1]}')
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            current_app.logger.error(f'Ошибка при работе с базой данных: {exc_type} : {exc_val}')

        if self.cursor:
            if exc_type:
                current_app.logger.debug(f'Rollback неудачной транзакции из базы данных: {exc_type} : {exc_val}')
                self.conn.rollback()
            else:
                # current_app.logger.debug(f'Commit удачной транзакции в базу данных')
                self.conn.commit()
                self.cursor.close()
                self.conn.close()
        return True  # всегда тру, тк все необходимые действия мы выполнили
