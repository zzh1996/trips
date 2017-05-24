from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FlightForm(Form):
    flightNum = StringField('航班号', validators=[DataRequired()])
    price = IntegerField('价格', validators=[DataRequired(), NumberRange(1)])
    numSeats = IntegerField('座位数', validators=[DataRequired(), NumberRange(1)])
    fromCity = StringField('出发城市', validators=[DataRequired()])
    arivCity = StringField('目的城市', validators=[DataRequired()])
    submit_btn = SubmitField('提交')


class HotelForm(Form):
    location = StringField('城市', validators=[DataRequired()])
    price = IntegerField('价格', validators=[DataRequired(), NumberRange(1)])
    numRooms = IntegerField('房间数', validators=[DataRequired(), NumberRange(1)])
    submit_btn = SubmitField('提交')


class CarForm(Form):
    location = StringField('城市', validators=[DataRequired()])
    price = IntegerField('价格', validators=[DataRequired(), NumberRange(1)])
    numCars = IntegerField('车辆数', validators=[DataRequired(), NumberRange(1)])
    submit_btn = SubmitField('提交')


class ReservationForm(Form):
    custName = StringField('客户姓名', validators=[DataRequired()])
    submit_btn = SubmitField('现在预定')


class CustomerForm(Form):
    custName = StringField('客户姓名', validators=[DataRequired()])
    submit_btn = SubmitField('提交')
