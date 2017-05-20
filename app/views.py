from flask import render_template, redirect, url_for, request, flash
from app import app
from app.models import *
from app.forms import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flight')
def flight_page():
    if request.args.get('from') and request.args.get('to'):
        frm=request.args.get('from')
        to=request.args.get('to')
        f=flights.query.filter(flights.fromCity==frm).filter(
            flights.arivCity==to).all()
    else:
        frm=''
        to=''
        f=flights.query.all()
    return render_template('flight.html',flights=f,frm=frm,to=to)

@app.route('/flight/delete/<int:id>')
def flight_delete(id):
    f = flights.query.get(id)
    reservations.query.filter(reservations.resvType == 'flight').filter(
        reservations.resvid == f.id).delete()
    f.delete()
    return redirect(url_for('flight_page'))

@app.route('/flight/edit/<int:id>', methods=['POST', 'GET'])
def flight_edit(id):
    if id==0:
        f=flights()
    else:
        f=flights.query.get(id)
    form=FlightForm(request.form,f)
    if request.method=='POST':
        if form.validate_on_submit():
            f.flightNum=form['flightNum'].data
            f.price=form['price'].data
            f.numSeats=form['numSeats'].data
            f.fromCity=form['fromCity'].data
            f.arivCity=form['arivCity'].data
            if id>0:
                f.numAvail = f.numSeats - reservations.query.filter(reservations.resvType == 'flight').filter(
                    reservations.resvid == f.id).count()
                if(f.numAvail)<0:
                    flash('座位数小于已预订数')
                    return render_template('flight_edit.html', form=form)
                f.save()
            else:
                f.numAvail=f.numSeats
                f.save()
            return redirect(url_for('flight_page'))
    return render_template('flight_edit.html',form=form)
