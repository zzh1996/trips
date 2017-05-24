from flask import render_template, redirect, url_for, request, flash, abort
from app import app, db
from app.models import *
from app.forms import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/flight')
def flight_page():
    if request.args.get('from') and request.args.get('to'):
        frm = request.args.get('from')
        to = request.args.get('to')
        f = flights.query.filter(flights.fromCity == frm).filter(
            flights.arivCity == to).all()
    else:
        frm = ''
        to = ''
        f = flights.query.all()
    return render_template('flight.html', flights=f, frm=frm, to=to)


@app.route('/flight/delete/<int:id>')
def flight_delete(id):
    f = flights.query.get(id)
    reservations.query.filter(reservations.resvType == 'flight').filter(
        reservations.resvid == f.id).delete()
    f.delete()
    return redirect(url_for('flight_page'))


@app.route('/flight/edit/<int:id>', methods=['POST', 'GET'])
def flight_edit(id):
    if id == 0:
        f = flights()
    else:
        f = flights.query.get(id)
    form = FlightForm(request.form, f)
    if request.method == 'POST':
        if form.validate_on_submit():
            f.flightNum = form['flightNum'].data
            f.price = form['price'].data
            f.numSeats = form['numSeats'].data
            f.fromCity = form['fromCity'].data
            f.arivCity = form['arivCity'].data
            if id > 0:
                f.numAvail = f.numSeats - reservations.query.filter(reservations.resvType == 'flight').filter(
                    reservations.resvid == f.id).count()
                if (f.numAvail) < 0:
                    flash('座位数小于已预订数')
                    return render_template('flight_edit.html', form=form)
                f.save()
            else:
                f.numAvail = f.numSeats
                f.save()
            return redirect(url_for('flight_page'))
    return render_template('flight_edit.html', form=form)


@app.route('/reservation')
def reservation_page():
    r = reservations.query.all()
    for row in r:
        if row.resvType == 'flight':
            f = flights.query.get(row.resvid)
            row.price = f.price
            row.location = f.fromCity + ' -> ' + f.arivCity
        elif row.resvType == 'hotel':
            h = hotels.query.get(row.resvid)
            row.price = h.price
            row.location = h.location
        elif row.resvType == 'car':
            c = cars.query.get(row.resvid)
            row.price = c.price
            row.location = c.location
    return render_template('reservation.html', reservations=r)


@app.route('/reservation/add/<int:type>/<int:id>', methods=['POST', 'GET'])
def reservation_add(type, id):
    form = ReservationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            r = reservations()
            if type == 0:
                r.resvType = 'flight'
                f = flights.query.get(id)
                if not f:
                    abort(404)
                if f.numAvail == 0:
                    flash('预定已满！')
                    return redirect(url_for('flight_page'))
                f.numAvail -= 1
                db.session.add(f)
            elif type == 1:
                r.resvType = 'hotel'
                h = hotels.query.get(id)
                if not h:
                    abort(404)
                if h.numAvail == 0:
                    flash('预定已满！')
                    return redirect(url_for('hotel_page'))
                h.numAvail -= 1
                db.session.add(h)
            elif type == 2:
                r.resvType = 'car'
                c = cars.query.get(id)
                if not c:
                    abort(404)
                if c.numAvail == 0:
                    flash('预定已满！')
                    return redirect(url_for('car_page'))
                c.numAvail -= 1
                db.session.add(c)
            else:
                return abort(404)
            r.resvid = id
            custName = form['custName'].data
            custid = customers.query.filter(customers.custName == custName).first().id
            if not custid:
                cust = customers()
                cust.custName = custName
                db.session.add(cust)
                db.session.flush()
                custid = cust.id
            r.custid = custid
            db.session.add(r)
            db.session.commit()
            return redirect(url_for('reservation_page'))
    return render_template('reservation_add.html', form=form)


@app.route('/reservation/delete/<int:id>')
def reservation_delete(id):
    r = reservations.query.get(id)
    db.session.delete(r)
    db.session.commit()
    return redirect(url_for('reservation_page'))


@app.route('/customer')
def customer_page():
    if request.args.get('name'):
        name = request.args.get('name')
        c = customers.query.filter(customers.custName.like('%' + name + '%')).all()
    else:
        name = ''
        c = customers.query.all()
    return render_template('customer.html', customers=c, name=name)


@app.route('/customer/edit/<int:id>', methods=['POST', 'GET'])
def customer_edit(id):
    c = customers.query.get(id)
    form = CustomerForm(request.form, c)
    if request.method == 'POST':
        if form.validate_on_submit():
            c.custName = form['custName'].data
            db.session.add(c)
            db.session.commit()
            return redirect(url_for('customer_page'))
    return render_template('customer_edit.html', form=form)


@app.route('/customer/delete/<int:id>')
def customer_delete(id):
    c = customers.query.get(id)
    reservations.query.filter(reservations.custid == id).delete()
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for('customer_page'))
