from iapi import db, session, Base, relationship

class Dealer(Base):
    '''Contains description of dealers. Data: id, name, city'''
    __tablename__ = 'dealers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=True)
    cars = relationship('Car', backref='dealer', cascade="all, delete-orphan") #wasted so much time on this

class Car(Base):
    '''Contains description of cars. Data: id, brand, model, vin, dealer_id'''
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    vin = db.Column(db.String(17), nullable=False)
    dealer_id = db.Column(db.Integer(), db.ForeignKey('dealers.id'), nullable=False)
