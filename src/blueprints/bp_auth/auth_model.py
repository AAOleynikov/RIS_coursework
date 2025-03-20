from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

from flask import current_app
from werkzeug.security import check_password_hash

from database.select import select_list


class AuthErrorType(Enum):
    SUCCESS = 0
    DB_CRITICAL_ERROR = 1
    INVALID_CREDENTIALS = 2
    UNKNOWN_ERROR = 99


@dataclass
class AuthResponse:
    user_group: str = None
    user_id: int = None
    error_message: str = None
    error_type: AuthErrorType = AuthErrorType.SUCCESS


def authenticate_user(db_config: Dict[str, Any], sql_provider, user_login, user_password) -> AuthResponse:
    _sql = sql_provider.get('get_auth_data.sql')
    current_app.logger.info(
        f"Попытка получить данные для авторизации пользователя с логином {user_login}")
    result, schema = select_list(db_config, _sql, (user_login,))
    if not schema and not result:
        current_app.logger.error(
            f"Ошибка при работе с базой данных при авторизации пользователя с логином {user_login}")
        error_message = "Критическая ошибка при работе с базой данных."
        return AuthResponse(
            error_message=error_message,
            error_type=AuthErrorType.DB_CRITICAL_ERROR)

    if not result:
        current_app.logger.info(
            f"Пользователь с логином {user_login} не был найден в базе данных.")
        error_message = "Пользователь не найден."
        return AuthResponse(
            error_message=error_message,
            error_type=AuthErrorType.INVALID_CREDENTIALS
        )

    stored_password_hash = result[0][0]
    user_group = result[0][1]
    user_id = result[0][2]

    if not check_password_hash(stored_password_hash, user_password):
        current_app.logger.info(
            f"Пользователь с логином {user_login} ввёл неверный пароль")
        error_message = "Неверный пароль."
        return AuthResponse(
            error_message=error_message,
            error_type=AuthErrorType.INVALID_CREDENTIALS
        )

    current_app.logger.info(
        f"Пользователь с логином {user_login} и ID:{user_id}/user_group:{user_group} был найден и пароль совпал")
    return AuthResponse(
        user_group=user_group,
        user_id=user_id,
        error_type=AuthErrorType.SUCCESS
    )
