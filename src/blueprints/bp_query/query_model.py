from flask import current_app
from dataclasses import dataclass
from typing import List, Optional, Tuple, Any

from database.select import select_list


@dataclass
class QueryInfoResponse:
    result: Optional[List[Tuple[Any, ...]]] = None
    schema: Optional[Tuple[str, ...]] = None
    error_message: str = ""
    status: bool = True


def universal_query_modeller(db_config: dict, sql_provider, sql_file: str, params: tuple) -> QueryInfoResponse:
    _sql = sql_provider.get(sql_file)
    result, schema = select_list(db_config, _sql, params)
    if not schema and not result:
        current_app.logger.error(f'Не удалось получить данные по параметризованному запросу из БД')
        error_msg = "Критическая ошибка при работе с БД."
        return QueryInfoResponse(error_message=error_msg, status=False)
    return QueryInfoResponse(result=result, schema=schema, error_message="", status=True)
