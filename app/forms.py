from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FlightForm(Form):
    flightNum = StringField('航班号', validators=[DataRequired()])
    price = IntegerField('价格', validators=[DataRequired(),NumberRange(1)])
    numSeats = IntegerField('座位数', validators=[DataRequired(),NumberRange(1)])
    fromCity = StringField('出发城市', validators=[DataRequired()])
    arivCity = StringField('目的城市', validators=[DataRequired()])
    submit_btn = SubmitField('提交')