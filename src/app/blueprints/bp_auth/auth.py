import os
from base64 import b64encode
from typing import Any

import requests
from flask import Blueprint, render_template, redirect, url_for, flash, session, current_app, request
from requests import RequestException

from access import login_required
from database.sql_provider import SQLProvider
from .auth_forms import LoginForm
from .auth_model import authenticate_user, AuthErrorType

blueprint_auth = Blueprint('bp_auth', __name__, template_folder='templates')

auth_sql_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/login', methods=['GET', 'POST'])
def login() -> Any:
    form = LoginForm()
    if form.validate_on_submit():
        if form.is_internal.data:  # True для внутреннего, False для внешнего
            current_app.logger.info(f"Попытка авторизации внутреннего пользователя с логином {form.login.data}")
            res_info = authenticate_user(
                db_config=current_app.config.get('db_config').get('not_authorized'),
                sql_provider=auth_sql_provider,
                user_login=form.login.data,
                user_password=form.password.data
            )
            if res_info.error_type == AuthErrorType.SUCCESS:
                current_app.logger.info(
                    f"Пользователь с логином {form.login.data} успешно авторизован с ID:{res_info.user_id} и user_group:{res_info.user_group}")
                current_app.logger.debug(
                    f"Сохранение данных пользователя с логином {form.login.data} в сессии и перенаправление в главное меню")
                return save_in_session_and_redirect(res_info.user_group, res_info.user_id)
            if res_info.error_type == AuthErrorType.DB_CRITICAL_ERROR:
                current_app.logger.info(
                    f"Пользователь с логином {form.login.data} не был авторизован из-за ошибки при работе с базой данных")
                flash("Ошибка на стороне сервера, попробуйте ещё раз позже", "danger")
            elif res_info.error_type == AuthErrorType.INVALID_CREDENTIALS:
                current_app.logger.info(
                    f"Пользователь с логином {form.login.data} не был авторизован из-за ошибки в логине или пароле")
                flash("Неверный логин или пароль, попробуйте снова", "danger")
            else:
                current_app.logger.error(
                    f"Пользователь с логином {form.login.data} не был авторизован из-за ошибки: {res_info.error_type}:{res_info.error_message}")
                flash("Ошибка на стороне сервера, попробуйте ещё раз позже", "danger")

        else:
            current_app.logger.info(f"Попытка авторизации внешнего пользователя с логином {form.login.data}")
            try:
                response = requests.get(
                    f'http://127.0.0.1:5002/find-user',
                    headers={'Authorization': create_basic_auth_token(form.login.data, form.password.data)}
                )
                resp_json = response.json()  # достали данные из тела ответа
                if resp_json['status'] == 200:
                    current_app.logger.info(
                        f"Пользователь с логином {form.login.data} успешно авторизован с ID:{resp_json['user_id']} и user_group:{resp_json['user_group']}")
                    return save_in_session_and_redirect(resp_json['user_group'], resp_json['user_id'])
                elif resp_json['status'] == 404 or resp_json['status'] == 401:
                    current_app.logger.info(
                        f"Пользователь с логином {form.login.data} не был авторизован из-за ошибки в логине или пароле")
                    flash("Неверный логин или пароль, попробуйте снова", "danger")
                elif resp_json['status'] == 400:
                    current_app.logger.info(
                        f"Пользователь с логином {form.login.data} не был авторизован из-за ошибки микросервиса: {resp_json['message']}")
                    flash("Ошибка на стороне сервера, попробуйте ещё раз позже", "danger")
                elif resp_json['status'] == 503:
                    current_app.logger.info(
                        f"Пользователь с логином {form.login.data} не был авторизован из-за ошибки работы микросервиса с базой данных: {resp_json['message']}")
                    flash("Ошибка на стороне сервера, попробуйте ещё раз позже", "danger")
                else:
                    current_app.logger.error(
                        f"Пользователь с логином {form.login.data} не был авторизован из-за ошибки: {resp_json['message']}")
                    flash("Ошибка на стороне сервера, попробуйте ещё раз позже", "danger")

            except RequestException as e:
                current_app.logger.error(
                    f"Пользователь с логином {form.login.data} не был авторизован из-за ошибки: {str(e)}")
                flash("Ошибка на стороне сервера, попробуйте ещё раз позже", "danger")

    elif request.method == 'POST':
        current_app.logger.info(
            f"Неудачная попытка авторизации пользователя: форма логина/пароля не прошла валидацию")
        flash("Пожалуйста, исправьте ошибки в форме.", "warning")
    return render_template('login.html', form=form)


@blueprint_auth.route('/logout')
@login_required
def logout() -> Any:
    current_app.logger.info(
        f"Пользователь ID:{session.get('user_id', "")}/user_group:{session.get('user_group', "")} деавторизуется из системы")
    current_app.logger.debug(
        f"Удаление сессии с пользователем ID:{session.get('user_id', "")}/user_group:{session.get('user_group', "")}")
    session.clear()
    flash("Вы успешно вышли из системы", "info")
    # return redirect(url_for('landing'))
    return redirect(url_for('bp_auth.login'))


def create_basic_auth_token(login, password):
    credentials_b64 = b64encode(f'{login}:{password}'.encode('ascii')).decode('ascii')
    token = f'Basic {credentials_b64}'
    return token


def save_in_session_and_redirect(user_group, user_id):
    current_app.logger.debug(
        f"Сохранение пользователя с ID:{user_id}/user_group:{user_group} в сессии и перенаправление его в главное меню")
    session['user_group'] = user_group
    session['user_id'] = user_id
    session.permanent = True
    return redirect(url_for('main_menu'))