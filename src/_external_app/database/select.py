from .DBcm import DBContextManager


def insert_test_report(db_config: dict, _sql_test_report: str, _sql_test_report_args: tuple, _sql_test: str,
                       _sql_test_args: tuple):
    try:
        with DBContextManager(db_config) as cursor:
            # Выполняем вставку заказа
            cursor.execute(_sql_test_report, _sql_test_report_args)
            # Получаем последний вставленный order_id
            test_report_id = cursor.lastrowid
            # Формируем данные для вставки в таблицу customer_order_list
            test_data = [
                (test_report_id, pt_id, test_status) for pt_id, test_status in _sql_test_args
            ]
            # Выполняем вставку позиций
            cursor.executemany(_sql_test, test_data)
            return True
    except Exception as e:

        raise


def select_list(db_config: dict, _sql: str, _sql_args: tuple):
    # with пытается создать экземпляром класса BDContextManager с помощью __init__ и сразу за ним __enter__
    result = ()
    schema = ()
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            cursor.execute(_sql, _sql_args)
            # результат вернётся в виде двумерного кортежа (неизменяемые)
            result = cursor.fetchall()
            schema = [item[0] for item in cursor.description]
    return result, schema


def select_dict(db_config: dict, _sql: str, _sql_args: tuple = ()):
    result, schema = select_list(db_config, _sql, _sql_args)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    return result_dict


def call_proc(db_config: dict, proc_name: str, proc_args: tuple):
    placeholders = ",".join(["%s"] * len(proc_args))
    _sql = f"CALL {proc_name}({placeholders});"
    result, _ = select_list(db_config, _sql, proc_args)
    return result[0]
