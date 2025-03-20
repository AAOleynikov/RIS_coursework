from datetime import datetime
from enum import Enum

from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange, ValidationError


class MonthChoices(Enum):
    JANUARY = (1, 'Январь')
    FEBRUARY = (2, 'Февраль')
    MARCH = (3, 'Март')
    APRIL = (4, 'Апрель')
    MAY = (5, 'Май')
    JUNE = (6, 'Июнь')
    JULY = (7, 'Июль')
    AUGUST = (8, 'Август')
    SEPTEMBER = (9, 'Сентябрь')
    OCTOBER = (10, 'Октябрь')
    NOVEMBER = (11, 'Ноябрь')
    DECEMBER = (12, 'Декабрь')


MONTH_CHOICES = [(month.value[0], month.value[1]) for month in MonthChoices]


def validate_year(form, field):
    current_year = datetime.now().year
    if field.data > current_year:
        raise ValidationError(f"Год не может быть позже текущего: {current_year}")


def validate_month(form, field):
    current_date = datetime.now()
    if form.year.data == current_date.year and field.data > current_date.month:
        raise ValidationError(f"Месяц не может быть позже текущего: {current_date.month}")


class ReportForm(FlaskForm):
    action = RadioField(
        'Действие',
        choices=[
            ('create', 'Создать новый отчёт'),
            ('view', 'Просмотреть существующий отчёт')
        ],
        default='view',
        validators=[DataRequired(message="Выбор действия обязателен")]
    )

    report_type = SelectField(
        'Выберите тип отчета',
        choices=[],
        validators=[DataRequired(message="Выбор отчета обязателен")]
    )

    year = IntegerField(
        'Год',
        validators=[
            DataRequired(message="Год обязателен"),
            NumberRange(min=2023, max=2100, message="Год должен быть в диапазоне 2023-2100"),
            validate_year
        ]
    )

    month = SelectField(
        'Месяц',
        choices=MONTH_CHOICES,
        coerce=int,
        validators=[
            DataRequired(message="Месяц обязателен"),
            validate_month
        ]
    )

    def __init__(self, reports=None, can_create_reports=None, can_view_reports=None, *args, **kwargs):
        """
        Инициализирует форму с динамическими выборками отчетов.

        :param reports: Список доступных отчетов.
        :param can_create_reports: Список идентификаторов отчетов, которые можно создать.
        :param can_view_reports: Список идентификаторов отчетов, которые можно просмотреть.
        """
        super().__init__(*args, **kwargs)
        self.create_choices = self._generate_choices(reports, can_create_reports)
        self.view_choices = self._generate_choices(reports, can_view_reports)
        self.update_report_choices()

    def _generate_choices(self, reports, allowed_reports):
        """
        Генерирует список выборов для отчетов на основе разрешений.

        :param reports: Список отчетов.
        :param allowed_reports: Список разрешенных идентификаторов отчетов.
        :return: Список кортежей для выборов.
        """
        if not reports or not allowed_reports:
            return []
        allowed_set = set(map(str, allowed_reports))
        return [
            (str(report['rep_id']), report['rep_name'])
            for report in reports
            if str(report['rep_id']) in allowed_set
        ]

    def update_report_choices(self):
        """
        Обновляет доступные варианты отчётов на основе выбранного действия.
        """
        if self.action.data == 'create':
            self.report_type.choices = self.create_choices
        else:
            self.report_type.choices = self.view_choices

    def validate_report_type(self, field):
        """
        Проверяет, что выбранный отчёт доступен пользователю на создание или просмотр.
        """
        selected_report = field.data
        if self.action.data == 'create':
            valid_reports = {choice[0] for choice in self.create_choices}
            if selected_report not in valid_reports:
                raise ValidationError("У вас нет прав для создания этого отчета.")
        elif self.action.data == 'view':
            valid_reports = {choice[0] for choice in self.view_choices}
            if selected_report not in valid_reports:
                raise ValidationError("У вас нет прав для просмотра этого отчета.")
