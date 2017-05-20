from app import db

class flights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flightNum = db.Column(db.String(20), unique=True, index=True)
    price = db.Column(db.Integer, index=True)
    numSeats = db.Column(db.Integer)
    numAvail = db.Column(db.Integer)
    fromCity = db.Column(db.String(20), index=True)
    arivCity = db.Column(db.String(20), index=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
    custName = db.Column(db.String(20), db.ForeignKey('customers.custName'), index=True)
    resvType = db.Column(db.Enum('flight','hotel','car'))
    resvid = db.Column(db.Integer)