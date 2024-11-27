# app/models.py

from app import db

class Airline(db.Model):
    __tablename__ = 'airlines'
    iata_code = db.Column(db.String(3), primary_key=True)
    airline = db.Column(db.String(100), nullable=False)

class Airport(db.Model):
    __tablename__ = 'airports'
    iata_code = db.Column(db.String(3), primary_key=True)
    airport = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100))
    country = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    airline = db.Column(db.String(3), db.ForeignKey('airlines.iata_code'), nullable=False)
    flight_number = db.Column(db.String(10), nullable=False)
    tail_number = db.Column(db.String(10))
    origin_airport = db.Column(db.String(3), db.ForeignKey('airports.iata_code'), nullable=False)
    destination_airport = db.Column(db.String(3), db.ForeignKey('airports.iata_code'), nullable=False)
    scheduled_departure = db.Column(db.Integer, nullable=False)
    departure_time = db.Column(db.Integer, nullable=False)    
    departure_delay = db.Column(db.Integer, nullable=False)
    taxi_out = db.Column(db.Integer)
    wheels_off = db.Column(db.DateTime)
    scheduled_time = db.Column(db.Integer)
    elapsed_time = db.Column(db.Integer)
    air_time = db.Column(db.Integer)
    distance = db.Column(db.Float)
    wheels_on = db.Column(db.DateTime)
    taxi_in = db.Column(db.Integer)
    scheduled_arrival = db.Column(db.DateTime)
    arrival_time = db.Column(db.DateTime)
    arrival_delay = db.Column(db.Integer)
    diverted = db.Column(db.Boolean, default=False)
    cancelled = db.Column(db.Boolean, default=False)
    cancellation_reason = db.Column(db.String(1))
    air_system_delay = db.Column(db.Integer)
    security_delay = db.Column(db.Integer)
    airline_delay = db.Column(db.Integer)
    late_aircraft_delay = db.Column(db.Integer)
    weather_delay = db.Column(db.Integer)
