import json
import os
from logging.config import dictConfig

from flask import Flask, render_template, request, session, url_for

from access import login_required
from blueprints.bp_auth.auth import blueprint_auth
from blueprints.bp_query.query import blueprint_query
from blueprints.bp_report.report import blueprint_report
from blueprints.bp_supply.supply import blueprint_supply

# конфигурирование app.logger (под капотом logging стандартный)
"""  
Уровни логирования:  
:DEBUG: Подробные сообщения для отладки, используется для диагностирования.  
:INFO: Стандартные сообщения, такие как успешное выполнение операции.  
:WARNING: Сообщения о потенциальных проблемах.  
:ERROR: Ошибки, которые могут повлиять на выполнение программы.  
:CRITICAL: Критические ошибки, которые требуют немедленного внимания.  
"""
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        # по умолчанию INFO
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

with open('data/db_connect.json') as f:
    app.config['db_config'] = json.load(f)

with open('data/db_access.json') as f:
    app.config['db_access'] = json.load(f)

with open('data/cache_config.json') as f:
    app.config['cache_config'] = json.load(f)

app.config['SECRET_KEY'] = os.urandom(30).hex()

app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_supply, url_prefix='/supply')


@app.route('/', methods=['GET'])
@login_required
def main_menu():
    user_role = session.get("user_group")
    access_rules = app.config["db_access"].get(user_role, {}).get('blueprints')
    accessible_blueprints = []
    if any("bp_query" in rule for rule in access_rules):
        accessible_blueprints.append({"url": url_for("bp_query.query_menu"), "name": "Меню запросов"})
    if any("bp_report" in rule for rule in access_rules):
        accessible_blueprints.append({"url": url_for("bp_report.report_menu"), "name": "Работа с отчётами"})
    if any("bp_supply" in rule for rule in access_rules):
        accessible_blueprints.append(
            {"url": url_for("bp_supply.supply_menu"), "name": "Провести поставку"})

    return render_template("main_menu.html", accessible_blueprints=accessible_blueprints, user_id=session.get('user_id'),
                           user_group=session.get('user_group'))


@app.route('/error', methods=['GET'])
def error_handler():
    error_message = request.args.get("error_message", "Ошибка при доступе к БД")
    return render_template("error.html", error_message=error_message,
                           user_id=session.get('user_id', '-'),
                           user_group=session.get('user_group', 'пользователь не авторизован')
                           )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
