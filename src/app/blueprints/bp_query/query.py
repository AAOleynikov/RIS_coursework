import json
import os

from flask import render_template, Blueprint, current_app, redirect, url_for, flash, session
from flask import request

from access import group_required
from database.sql_provider import SQLProvider

# Должно быть обязательно!!!!
#from query_forms import EquipmentStatusForm, SpecialistReportForm
#from .query_model import universal_query_modeller
from .query_forms import SearchInvoicedProductsByDateRangeForm, SearchInvoicedProductsBySupplierForm
from .query_model import universal_query_modeller

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

query_sql_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

with open(os.path.join(os.path.dirname(__file__), 'data', 'queries.json'), encoding='utf-8') as f:
    queries = json.load(f)


@blueprint_query.route('/', methods=['GET'])
@group_required
def query_menu():
    current_app.logger.info(
        f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} начал работать с Меню запросов")
    accessible_queries = [
        query for query in queries
        if (
               access_rule := current_app.config['db_access']
               .get(session.get('user_group', ''), {})
               .get('blueprints', {})
               .get('bp_query', {})
               .get('accessible_queries', [])
           ) == ["all"] or query.get("query_id") in access_rule
    ]
    current_app.logger.info(
        f"Пользователю ID:{session.get('user_id')}/user_group:{session.get('user_group')} будут показаны запросы:{accessible_queries}")
    return render_template("query_menu.html", accessible_queries=accessible_queries,
                           user_id=session.get('user_id'), user_group=session.get('user_group'))


@blueprint_query.route('/query', methods=['GET', 'POST'])
@group_required
def universal_query_controller():
    if request.method == 'GET':
        query_id = request.args.get('query_id')
        current_app.logger.info(
            f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} начал работать с запросом ID:{query_id}")
    else:
        query_id = request.form.get('query_id')
        current_app.logger.info(
            f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} прислал данные для параметризованного запроса с ID:{query_id}")

    accessible_queries = [
        query for query in queries
        if (
               access_rule := current_app.config['db_access']
               .get(session.get('user_group', ''), {})
               .get('blueprints', {})
               .get('bp_query', {})
               .get('accessible_queries', [])
           ) == ["all"] or query.get("query_id") in access_rule
    ]

    query = next((q for q in accessible_queries if str(q.get('query_id')) == str(query_id)), None)
    if not query:
        current_app.logger.info(
            f"Пользователю ID:{session.get('user_id')}/user_group:{session.get('user_group')} был отвергнут доступ системой к параметризованному запросу с ID:{query_id}")
        return redirect(url_for('error_handler', error_message="Запрос не найден или не доступен вам"))

    form = globals().get(query.get('query_form'))()
    if form.validate_on_submit():
        current_app.logger.debug(
            f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} ввёл корректные параметры запроса ID:{query_id}, обращение к моделлеру запроса: {query.get('query_model')}")
        response = globals().get(query.get('query_model'))(
            db_config=current_app.config.get('db_config').get(str(session.get('user_group'))),
            sql_file=query.get('sql'), sql_provider=query_sql_provider,
            params=tuple(form.data.get(param) for param in
                         query.get('sql_params') if
                         param in form.data))

        if response.status:
            current_app.logger.info(
                f"Пользователю ID:{session.get('user_id')}/user_group:{session.get('user_group')} будут отображены результаты параметризованного запроса {query_id}")
            return render_template(
                'query_result.html',
                title="Результаты поиска",
                headers=query.get('schema_ru'),
                results=response.result,
                query_controller_url=url_for('bp_query.' + query.get('query_controller'),
                                             query_id=query.get('query_id')),
                user_id=session.get('user_id'), user_group=session.get('user_group'), query_name=query.get('query_name')
            )
        else:
            current_app.logger.info(
                f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} во время выполнения параметризованного запроса {query_id} возникла ошибка {response.error_message}")
            flash(response.error_message, "error")
            return redirect(url_for('bp_query.' + query.get('query_controller'), query_id=query_id))

    elif request.method == 'POST':
        current_app.logger.info(
            f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} прислал некорректную форму для выполнения параметризованного запроса {query_id}")
        flash("Пожалуйста, исправьте ошибки в форме.", "error")

    return render_template("query_input.html", title="Поиск по категории продуктов", form=form, query_id=query_id,
                           user_id=session.get('user_id'), user_group=session.get('user_group'),
                           query_name=query.get('query_name'))
