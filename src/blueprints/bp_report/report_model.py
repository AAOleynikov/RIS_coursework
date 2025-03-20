from dataclasses import dataclass
from typing import List, Optional

from database.select import select_list, call_proc


@dataclass
class ReportResponse:
    result: Optional[List[dict]] = None
    schema: Optional[List[dict]] = None
    error_message: str = ""
    error_type: int = 0


def create_monthly_report(db_config: dict, report: dict, year: int, month: int) -> ReportResponse:
    proc_name = report.get('proc_name')
    result = call_proc(db_config, proc_name, (year, month))
    if result[0] != 0:
        return ReportResponse(error_message=result[1], error_type=result[0])
    return ReportResponse()


def view_monthly_report(db_config: dict, sql_provider, report: dict, year: int, month: int) -> ReportResponse:
    _sql = sql_provider.get(str(report.get('sql_get')))
    result, schema = select_list(db_config, _sql, (year, month))
    if not schema:
        error_msg = "Критическая ошибка: Выполнить запрос не удалось."
        return ReportResponse(error_message=error_msg, error_type=3)
    if not result:
        error_msg = "Отчёт не существует."
        return ReportResponse(error_message=error_msg, error_type=4)
    if result[0][0] is None:
        error_msg = "Отчёт существует, но не имеет данных для отображения."
        return ReportResponse(error_message=error_msg, error_type=2)
    return ReportResponse(result=result, schema=report.get('schema'))
