from functools import wraps

from flask import session, request, redirect, url_for, current_app


def login_required(func):
    @wraps(func)
    def wrapper(*argc, **kwargs):
        if 'user_group' in session:
            return func(*argc, **kwargs)
        else:
            return redirect(url_for('bp_auth.login'))
    return wrapper


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_role = session.get('user_group')
        if not user_role:
            return redirect(url_for('bp_auth.login'))

        # Получаем текущий эндпоинт (например, 'bp_query.query_menu' или 'main_menu')
        user_request = request.endpoint
        user_bp = user_request.split('.')[0] if '.' in user_request else user_request  # Имя блюпринта или страницы
        user_handler = user_request.split('.')[1] if '.' in user_request else None  # Обработчик, если есть

        role_access = current_app.config['db_access'].get(user_role, {})

        if user_request in role_access.get("pages", []):
            return func(*args, **kwargs)

        if user_handler in role_access.get("pages", []):
            return func(*args, **kwargs)

        blueprints = role_access.get("blueprints", {})
        if user_bp in blueprints:
            bp_access = blueprints[user_bp]

            # Если доступ ко всему блюпринту
            if bp_access == ["all"]:
                return func(*args, **kwargs)

            # Если указан доступ к конкретным обработчикам
            if isinstance(bp_access, dict) and user_handler:
                # Проверка доступа к страницам блюпринта
                if user_handler in bp_access.get("pages", []):
                    return func(*args, **kwargs)

        return redirect(url_for('error_handler', error_message="У вас нет прав для доступа к этой странице."))

    return wrapper
