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
    db.session.delete(f)
    db.session.commit()
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
            else:
                f.numAvail = f.numSeats
            db.session.add(f)
            db.session.commit()
            return redirect(url_for('flight_page'))
    return render_template('flight_edit.html', form=form)


@app.route('/hotel')
def hotel_page():
    if request.args.get('location'):
        loc = request.args.get('location')
        h = hotels.query.filter(hotels.location == loc).all()
    else:
        loc = ''
        h = hotels.query.all()
    return render_template('hotel.html', hotels=h, loc=loc)


@app.route('/hotel/delete/<int:id>')
def hotel_delete(id):
    h = hotels.query.get(id)
    reservations.query.filter(reservations.resvType == 'hotel').filter(
        reservations.resvid == h.id).delete()
    db.session.delete(h)
    db.session.commit()
    return redirect(url_for('hotel_page'))


@app.route('/hotel/edit/<int:id>', methods=['POST', 'GET'])
def hotel_edit(id):
    if id == 0:
        h = hotels()
    else:
        h = hotels.query.get(id)
    form = HotelForm(request.form, h)
    if request.method == 'POST':
        if form.validate_on_submit():
            h.location = form['location'].data
            h.price = form['price'].data
            h.numRooms = form['numRooms'].data
            if id > 0:
                h.numAvail = h.numRooms - reservations.query.filter(reservations.resvType == 'hotel').filter(
                    reservations.resvid == h.id).count()
                if (h.numAvail) < 0:
                    flash('房间数小于已预订数')
                    return render_template('hotel_edit.html', form=form)
            else:
                h.numAvail = h.numRooms
            db.session.add(h)
            db.session.commit()
            return redirect(url_for('hotel_page'))
    return render_template('hotel_edit.html', form=form)


@app.route('/car')
def car_page():
    if request.args.get('location'):
        loc = request.args.get('location')
        c = cars.query.filter(cars.location == loc).all()
    else:
        loc = ''
        c = cars.query.all()
    return render_template('car.html', cars=c, loc=loc)


@app.route('/car/delete/<int:id>')
def car_delete(id):
    c = cars.query.get(id)
    reservations.query.filter(reservations.resvType == 'car').filter(
        reservations.resvid == c.id).delete()
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for('car_page'))


@app.route('/car/edit/<int:id>', methods=['POST', 'GET'])
def car_edit(id):
    if id == 0:
        c = cars()
    else:
        c = cars.query.get(id)
    form = CarForm(request.form, c)
    if request.method == 'POST':
        if form.validate_on_submit():
            c.location = form['location'].data
            c.price = form['price'].data
            c.numCars = form['numCars'].data
            if id > 0:
                c.numAvail = c.numCars - reservations.query.filter(reservations.resvType == 'car').filter(
                    reservations.resvid == c.id).count()
                if (c.numAvail) < 0:
                    flash('车辆数小于已预订数')
                    return render_template('car_edit.html', form=form)
            else:
                c.numAvail = c.numCars
            db.session.add(c)
            db.session.commit()
            return redirect(url_for('car_page'))
    return render_template('car_edit.html', form=form)


@app.route('/reservation')
def reservation_page():
    r = reservations.query.all()
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
            cust = customers.query.filter(customers.custName == custName).first()
            if not cust:
                cust = customers()
                cust.custName = custName
                db.session.add(cust)
                db.session.flush()
            r.custid = cust.id
            db.session.add(r)
            db.session.commit()
            return redirect(url_for('reservation_page'))
    return render_template('reservation_add.html', form=form)


@app.route('/reservation/delete/<int:id>')
def reservation_delete(id):
    r = reservations.query.get(id)
    r.delete()
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


@app.route('/customer/detail/<int:id>')
def customer_detail(id):
    c = customers.query.get(id)
    rs = reservations.query.filter(reservations.custid == id).all()
    totalprice = sum([r.price() for r in rs])
    return render_template('customer_detail.html', customer=c, reservations=rs, totalprice=totalprice)


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
    for r in reservations.query.filter(reservations.custid == id).all():
        r.delete()
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for('customer_page'))
