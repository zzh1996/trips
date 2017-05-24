from app import db


class flights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flightNum = db.Column(db.String(20), unique=True, index=True)
    price = db.Column(db.Integer, index=True)
    numSeats = db.Column(db.Integer)
    numAvail = db.Column(db.Integer)
    fromCity = db.Column(db.String(20), index=True)
    arivCity = db.Column(db.String(20), index=True)


class hotels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(20), unique=True, index=True)
    price = db.Column(db.Integer, index=True)
    numRooms = db.Column(db.Integer)
    numAvail = db.Column(db.Integer)


class cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(20), unique=True, index=True)
    price = db.Column(db.Integer, index=True)
    numCars = db.Column(db.Integer)
    numAvail = db.Column(db.Integer)


class customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    custName = db.Column(db.String(20), unique=True, index=True)


class reservations(db.Model):
    resvKey = db.Column(db.Integer, primary_key=True)
    custid = db.Column(db.Integer, db.ForeignKey('customers.id'), index=True)
    resvType = db.Column(db.Enum('flight', 'hotel', 'car'))
    resvid = db.Column(db.Integer)
    customer = db.relationship('customers', backref=db.backref('reservations'))

    def location(self):
        if self.resvType == 'flight':
            f = flights.query.get(self.resvid)
            return f.flightNum+'('+f.fromCity + '->' + f.arivCity+')'
        elif self.resvType == 'hotel':
            h = hotels.query.get(self.resvid)
            return  h.location
        elif self.resvType == 'car':
            c = cars.query.get(self.resvid)
            return c.location

    def price(self):
        if self.resvType == 'flight':
            f = flights.query.get(self.resvid)
            return f.price
        elif self.resvType == 'hotel':
            h = hotels.query.get(self.resvid)
            return h.price
        elif self.resvType == 'car':
            c = cars.query.get(self.resvid)
            return c.price

    def type(self):
        return {'flight':'航班','hotel':'宾馆','car':'出租车'}[self.resvType]

    def delete(self):
        if self.resvType == 'flight':
            f = flights.query.get(self.resvid)
            f.numAvail+=1
            db.session.add(f)
        elif self.resvType == 'hotel':
            h = hotels.query.get(self.resvid)
            h.numAvail += 1
            db.session.add(h)
        elif self.resvType == 'car':
            c = cars.query.get(self.resvid)
            c.numAvail += 1
            db.session.add(c)
        db.session.delete(self)