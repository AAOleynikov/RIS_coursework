from flask import current_app

from .DBcm import DBContextManager

def confirm_invoice(db_config: dict, _sql_update_invoice_status: str, _sql_update_invoice_status_args: tuple,
                       _sql_update_product_capacity: str, _sql_update_product_capacity_args: tuple):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(_sql_update_invoice_status, _sql_update_invoice_status_args)

        cursor.execute(_sql_update_product_capacity, _sql_update_product_capacity_args)

        return True
    return False

def insert_invoice(db_config: dict, _sql_invoice: str, _sql_invoice_args: tuple,
                       _sql_product_in_invoice: str, _sql_product_in_invoice_args: tuple):
         with DBContextManager(db_config) as cursor:
            if cursor is None:
                raise ValueError('Курсор не создан')

            cursor.execute(_sql_invoice, _sql_invoice_args)
            invoice_id = cursor.lastrowid

            pii_data = [
                (pr_id, pr_count, pr_price, invoice_id) for pr_id, pr_count, pr_price in _sql_product_in_invoice_args
            ]

            cursor.executemany(_sql_product_in_invoice, pii_data)
            return True
         return False

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
    print(result)
    return result[0]