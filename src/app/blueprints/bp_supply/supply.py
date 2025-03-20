import datetime
import os

from flask import Blueprint, request, render_template, redirect, url_for, session, flash, current_app

from access import group_required
from cache.wrapper import fetch_from_cache
from database.select import select_dict
from database.sql_provider import SQLProvider
from .supply_model import save_invoice_model, work_with_invoices_model, confirm_invoice_model, get_invoice_model

blueprint_supply = Blueprint('bp_supply', __name__, template_folder='templates')

supply_sql_provider = SQLProvider(
    os.path.join(os.path.dirname(__file__), 'sql')
)

@blueprint_supply.route('/', methods=['GET', 'POST'])
@group_required
def supply_menu():
    current_app.logger.info(
        f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} начал работать с Меню поставок")
    access_rules = current_app.config['db_access'].get(session.get('user_group'), {}).get('blueprints', {}).get('bp_supply', {}).get("pages", [])
    available_actions = []
    if "make_invoice" in access_rules:
        available_actions.append({"url": url_for("bp_supply.make_invoice"), "name": "Заполнить накладную с поставкой"})
    if "work_with_invoices" in access_rules:
        available_actions.append({"url": url_for("bp_supply.work_with_invoices"), "name": "Подтвердить поставки по накладным"})
    return render_template("supply_menu.html", available_actions=available_actions,
                           user_id=session.get('user_id'), user_group=session.get('user_group'))

@blueprint_supply.route('/make_invoice', methods=['GET'])
@group_required
def make_invoice():
    cache_config = current_app.config['cache_config']
    db_config = current_app.config['db_config'].get(session.get('user_group'))
    cache_select_dict_products = fetch_from_cache(f'products', cache_config)(select_dict)

    _sql = supply_sql_provider.get('get_products.sql')
    products = cache_select_dict_products(db_config, _sql)

    invoiced_products = session.get("invoice", {})

    return render_template("make_invoice.html", products=products,
                           invoiced_products=invoiced_products,
                           user_id=session.get('user_id'), user_group=session.get('user_group'))

@blueprint_supply.route('/update_invoice', methods=['POST'])
@group_required
def update_invoice():
    prod_id = request.form.get('product_id')
    current_invoice = session.get('invoice', {})
    current_invoice[prod_id] = {}
    session['invoice'] = current_invoice
    return redirect(url_for('bp_supply.make_invoice'))

@blueprint_supply.route('/update_invoice_product', methods=['POST'])
@group_required
def update_invoice_product():
    prod_id = request.form.get('product_id')
    prod_price = request.form.get('product_price')
    prod_count = request.form.get('product_count')
    current_invoice = session.get('invoice', {})
    current_invoice[prod_id] = {"price" : prod_price, "count" : prod_count}
    session['invoice'] = current_invoice
    return redirect(url_for('bp_supply.make_invoice'))

@blueprint_supply.route('/delete_invoice_product', methods=['POST'])
@group_required
def delete_invoice_product():
    prod_id = request.form.get('product_id')
    current_invoice = session.get('invoice', {})
    del current_invoice[prod_id]
    session['invoice'] = current_invoice
    return redirect(url_for('bp_supply.make_invoice'))

@blueprint_supply.route('/clear_invoice', methods=['GET'])
@group_required
def clear_invoice():
    session.pop('invoice', None)
    return redirect(url_for('bp_supply.make_invoice'))

@blueprint_supply.route('/save_invoice', methods=['GET'])
@group_required
def save_invoice():
    current_invoice = session.get('invoice')
    if not current_invoice:
        flash("Накладная пуста. Нечего сохранять.", "danger")
        return redirect(url_for('bp_supply.make_invoice'))

    for product_id, product in current_invoice.items():
        if not product or not product.get('price') or not product.get('count'):
            flash("Для всех товаров в накладной необходимо указать количество и цену", "danger")
            return redirect(url_for('bp_supply.make_invoice'))

    db_config = current_app.config['db_config'].get(session.get('user_group'))

    response = save_invoice_model(db_config, supply_sql_provider, 'save_invoice.sql',
                                      'save_product_in_invoice.sql',
                                  session.get('user_id'), current_invoice)

    if response.error_message:
        flash("При сохранении накладной возникла критическая ошибка на стороне сервера, попробуйте ещё раз позже.",
              "danger")
        return redirect(url_for('bp_supply.make_invoice'))

    session.pop('invoice')
    flash("Накладная успешно сохранена!", "success")
    return redirect(url_for('bp_supply.make_invoice'))

@blueprint_supply.route('/work_with_invoices', methods=['GET', 'POST'])
@group_required
def work_with_invoices():
    db_config = current_app.config['db_config'].get(session.get('user_group'))
    if request.method == 'GET':
        response = work_with_invoices_model(db_config, supply_sql_provider, 'get_unconfirmed_invoices.sql')
        if response.error_message:
            flash("При получении неподтверждённых накладных поставок возникла критическая ошибка на стороне сервера, попробуйте ещё раз позже.",
                  "danger")
            return redirect(url_for('bp_supply.supply_menu'))
        if not response.result:
            flash(
                "Все накладные уже проверены! Отличная работа!",
                "success")
        return render_template("work_with_invoices.html", invoices=response.result,
                               user_id=session.get('user_id'), user_group=session.get('user_group'))
    else:
        invoice_id = request.form.get('invoice_id')
        response = get_invoice_model(db_config, supply_sql_provider, 'get_invoice_data.sql', invoice_id)
        if response.error_message:
            flash("При получении неподтверждённых накладных поставок возникла критическая ошибка на стороне сервера, попробуйте ещё раз позже.",
                  "danger")
            return redirect(url_for('bp_supply.work_with_invoices'))
        return render_template("confirm_invoice.html", invoice_id=invoice_id, invoice_products=response.result,
                               user_id=session.get('user_id'), user_group=session.get('user_group'))

@blueprint_supply.route('/confirm_invoice', methods=['POST'])
@group_required
def confirm_invoice():
    invoice_id = request.form.get('invoice_id')
    db_config = current_app.config['db_config'].get(session.get('user_group'))
    response = confirm_invoice_model(db_config, supply_sql_provider, 'update_invoice_status.sql', 'update_product_capacity.sql', invoice_id)
    if response.error_message:
        flash(
            "При получении неподтверждённых накладных поставок возникла критическая ошибка на стороне сервера, попробуйте ещё раз позже.",
            "danger")
    else:
        flash("Данные по накладной и запасам на складе успешно обновлены",
                "success")
    return redirect(url_for('bp_supply.work_with_invoices'))