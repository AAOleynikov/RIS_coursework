import json
import os

from flask import Blueprint, render_template, flash, session, current_app, request

from access import group_required
from database.sql_provider import SQLProvider
from .report_forms import ReportForm
from .report_model import create_monthly_report, view_monthly_report

# Определение Blueprint
blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
auth_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

with open(os.path.join(os.path.dirname(__file__), 'data', 'reports.json'), encoding='utf-8') as f:
    reports = json.load(f)


@blueprint_report.route('/report_menu', methods=['GET', 'POST'])
@group_required
def report_menu():
    current_app.logger.info(
        f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} начал работать с Меню отчётов")
    group_access = current_app.config['db_access'].get(session.get('user_group'), {}).get("blueprints", {}).get(
        "bp_report", {})
    permissions = group_access.get("permissions", {})
    can_create_reports = set(map(int, permissions.get("can_create_reports", [])))
    can_view_reports = set(map(int, permissions.get("can_view_reports", [])))
    current_app.logger.info(
        f"Пользователю ID:{session.get('user_id')}/user_group:{session.get('user_group')} доступны отчёты на просмотр:{can_view_reports} и отчёты на создание {can_create_reports}")

    form = ReportForm(reports=reports, can_create_reports=can_create_reports, can_view_reports=can_view_reports)
    if form.validate_on_submit():
        selected_report_id = form.report_type.data
        selected_action = form.action.data
        year = form.year.data
        month = form.month.data

        # Поиск выбранного отчета в данных
        selected_report = next((r for r in reports if str(r["rep_id"]) == selected_report_id), None)

        if selected_action == 'create':
            current_app.logger.info(
                f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} начал создание отчёта с ID:{selected_report_id} за период {year}.{month}")
            # Логика создания отчета
            response = create_monthly_report(
                db_config=current_app.config.get('db_config').get(session.get('user_group')),
                report=selected_report,
                year=year,
                month=month
            )
            if response.error_message:
                current_app.logger.info(
                    f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} не смог создать отчёт с ID:{selected_report_id} за период {year}.{month} по причине: {response.error_message}")
                flash(response.error_message, "danger")
            else:
                current_app.logger.info(
                    f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} успешно создал отчёт с ID:{selected_report_id} за период {year}.{month}")
                flash("Отчет успешно создан.", "success")

        else:
            current_app.logger.info(
                f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} начал просмотр отчёта с ID:{selected_report_id} за период {year}.{month}")

            # Логика просмотра отчета
            response = view_monthly_report(
                db_config=current_app.config.get('db_config').get(session.get('user_group')),
                sql_provider=auth_provider,
                report=selected_report,
                year=year,
                month=month
            )
            if response.error_message:
                current_app.logger.info(
                    f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} не смог просмотерть отчёт с ID:{selected_report_id} за период {year}.{month} по причине: {response.error_message}")
                flash(response.error_message, "danger")
            else:
                current_app.logger.info(
                    f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} смог просмотреть отчёт с ID:{selected_report_id} за период {year}.{month}")
                return render_template(
                    "report_view.html",
                    title=f'Просмотр отчета "{selected_report.get('rep_name')}" за {year}.{month}',
                    headers=response.schema,
                    results=response.result,
                    user_group=session.get('user_group'),
                    user_id=session.get('user_id')
                )

    elif request.method == 'POST':
        current_app.logger.info(
            f"Пользователь ID:{session.get('user_id')}/user_group:{session.get('user_group')} ввёл некорректные данные формы Меню отчётов")
        flash("Пожалуйста, исправьте ошибки в форме.", "error")

    return render_template("report_menu.html", title="Работа с отчётами", form=form,
                           user_group=session.get('user_group'),
                           user_id=session.get('user_id'))
