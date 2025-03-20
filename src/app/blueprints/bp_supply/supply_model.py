import datetime
from dataclasses import dataclass
from typing import List, Optional

from database.select import select_list, insert_invoice, confirm_invoice

@dataclass
class SupplyResponse:
    result: Optional[List[dict]] = None
    schema: Optional[List[dict]] = None
    error_message: str = ""
    error_type: int = 0

def confirm_invoice_model(db_config: dict, sql_provider,
                          file_update_invoice_status: str, file_update_product_capacity: str,
                          invoice_id: int):

    update_invoice_status = sql_provider.get(file_update_invoice_status)
    update_product_capacity = sql_provider.get(file_update_product_capacity)

    if confirm_invoice(db_config, update_invoice_status, (invoice_id,),
                       update_product_capacity, (invoice_id,)):
        return SupplyResponse()

    error_msg = "Не удалось выполнить операцию вставки"
    return SupplyResponse(error_message=error_msg, error_type=1)

def get_invoice_model(db_config: dict, sql_provider,  file_get_invoice_data: str, invoice_id) -> SupplyResponse:
    _get_invoice_data = sql_provider.get(file_get_invoice_data)
    result, schema = select_list(db_config, _get_invoice_data, (invoice_id,))
    if not schema:
        error_msg = "Не удалось получить данные из БД"
        return SupplyResponse(error_message=error_msg, error_type=1)
    return SupplyResponse(result, schema)

def work_with_invoices_model(db_config: dict, sql_provider, file_sql_unconfirmed_invoice: str) -> SupplyResponse:
    _sql = sql_provider.get(file_sql_unconfirmed_invoice)
    result, schema = select_list(db_config, _sql, ())
    if not schema:
        error_msg = "Не удалось получить данные из БД"
        return SupplyResponse(error_message=error_msg, error_type=1)
    return SupplyResponse(result, schema)

def save_invoice_model(db_config: dict, sql_provider, file_sql_invoice: str, file_sql_product_in_invoice: str,
                           supplier_id, selected_products) -> SupplyResponse:
    invoice_save_date = datetime.datetime.now().strftime('%Y-%m-%d')
    _sql_invoice = sql_provider.get(file_sql_invoice)
    _sql_product_in_invoice = sql_provider.get(file_sql_product_in_invoice)

    _sql_product_in_invoice_params = []
    inv_all_cost = 0

    for product_id, product in selected_products.items():
        _sql_product_in_invoice_params.append([product_id, product['count'], product['price']])
        inv_all_cost += int(product['count']) * int(product['price'])

    _sql_invoice_params = (supplier_id, invoice_save_date, inv_all_cost, 0,)

    if insert_invoice(db_config, _sql_invoice, _sql_invoice_params, _sql_product_in_invoice, _sql_product_in_invoice_params):
        return SupplyResponse()

    error_msg = "Не удалось выполнить операцию вставки"
    return SupplyResponse(error_message=error_msg, error_type=1)