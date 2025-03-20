from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """
    Форма для аутентификации пользователя.
    """
    login = StringField(
        'Логин',
        validators=[
            DataRequired(message="Введите ваш логин."),
            Length(min=3, max=64, message="Логин должен быть от 3 до 64 символов.")
        ],
        render_kw={"placeholder": "Введите ваш логин"}
    )

    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(message="Введите ваш пароль."),
            Length(min=4, max=64, message="Пароль должен быть от 4 до 64 символов.")
        ],
        render_kw={"placeholder": "Введите ваш пароль"}
    )

    is_internal = BooleanField(
        'Я сотрудник',
        default=True,  # Установить внутреннего пользователя по умолчанию
    )
