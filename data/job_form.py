from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader = IntegerField("Лидер", validators=[DataRequired()])
    job = StringField("Название работы", validators=[DataRequired()])
    work_size = IntegerField("Объём работы в часах", validators=[DataRequired()])
    collaborators = StringField('Список участников через пробел')
    is_finished = BooleanField("Завершено?")
    submit = SubmitField('Добавить')
