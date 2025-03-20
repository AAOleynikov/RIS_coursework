from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField
from wtforms.validators import DataRequired

class SearchInvoicedProductsByDateRangeForm(FlaskForm):
    start_date = DateField("Начальная дата", format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField("Конечная дата", format='%Y-%m-%d', validators=[DataRequired()])

class SearchInvoicedProductsBySupplierForm(FlaskForm):
    sup_id = IntegerField("ID поставщика", validators=[DataRequired()])