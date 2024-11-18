import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Validar que las variables necesarias están definidas
required_env_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_NAME']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Faltan variables de entorno requeridas: {', '.join(missing_vars)}")

# Configurar aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos desde variables de entorno
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT', '3306')

# Construir la URL de conexión
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Modelos
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
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)


class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)  # Año del vuelo
    month = db.Column(db.Integer, nullable=False)  # Mes del vuelo
    day = db.Column(db.Integer, nullable=False)  # Día del mes del vuelo
    day_of_week = db.Column(db.Integer, nullable=False)  # Día de la semana (1=Lunes, 7=Domingo)
    airline = db.Column(db.String(3), db.ForeignKey('airlines.iata_code'), nullable=True)  # Código de la aerolínea
    flight_number = db.Column(db.String(10), nullable=False)  # Número del vuelo
    tail_number = db.Column(db.String(10))  # Número de registro del avión
    origin_airport = db.Column(db.String(3), db.ForeignKey('airports.iata_code'), nullable=True)  # Aeropuerto de origen
    destination_airport = db.Column(db.String(3), db.ForeignKey('airports.iata_code'), nullable=True)  # Aeropuerto de destino
    
    # Usar String para horarios como "0225" o "2359"
    scheduled_departure = db.Column(db.String(4), nullable=False)  # Salida programada (hhmm)
    departure_time = db.Column(db.String(4))  # Hora real de salida (hhmm)
    wheels_off = db.Column(db.String(4))  # Hora en la que el avión despegó (hhmm)
    wheels_on = db.Column(db.String(4))  # Hora en la que aterrizó (hhmm)
    scheduled_arrival = db.Column(db.String(4))  # Llegada programada (hhmm)
    arrival_time = db.Column(db.String(4))  # Hora real de llegada (hhmm)

    departure_delay = db.Column(db.Integer, nullable=True)  # Retraso en la salida (minutos, negativo si salió antes)
    taxi_out = db.Column(db.Integer)  # Tiempo de rodaje hasta despegar (minutos)
    scheduled_time = db.Column(db.Integer)  # Tiempo programado de vuelo (minutos)
    elapsed_time = db.Column(db.Integer)  # Tiempo total transcurrido (minutos)
    air_time = db.Column(db.Integer)  # Tiempo en el aire (minutos)
    taxi_in = db.Column(db.Integer)  # Tiempo de rodaje tras aterrizar (minutos)
    arrival_delay = db.Column(db.Integer)  # Retraso en la llegada (minutos, negativo si llegó antes)
    
    distance = db.Column(db.Float)  # Distancia entre aeropuertos (millas)
    
    diverted = db.Column(db.Boolean, default=False)  # Si el vuelo fue desviado (1 = sí, 0 = no)
    cancelled = db.Column(db.Boolean, default=False)  # Si el vuelo fue cancelado (1 = sí, 0 = no)
    cancellation_reason = db.Column(db.String(1))  # Razón de cancelación (A, B, C, etc.)
    
    # Retrasos específicos (minutos)
    air_system_delay = db.Column(db.Integer)  # Retraso por sistema aéreo
    security_delay = db.Column(db.Integer)  # Retraso por seguridad
    airline_delay = db.Column(db.Integer)  # Retraso por aerolínea
    late_aircraft_delay = db.Column(db.Integer)  # Retraso por avión tardío
    weather_delay = db.Column(db.Integer)  # Retraso por condiciones climáticas


# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/airlines', methods=['GET', 'POST'])
def handle_airlines():
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'iata_code' not in data or 'airline' not in data:
            return jsonify({'error': 'Datos incompletos o inválidos'}), 400
        try:
            airline = Airline(
                iata_code=data['iata_code'],
                airline=data['airline']
            )
            db.session.add(airline)
            db.session.commit()
            return jsonify({'message': 'Airline added successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        airlines = Airline.query.all()
        return jsonify([{'iata_code': a.iata_code, 'airline': a.airline} for a in airlines])

@app.route('/api/airports', methods=['GET', 'POST'])
def handle_airports():
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'iata_code' not in data or 'airport' not in data or 'city' not in data:
            return jsonify({'error': 'Datos incompletos o inválidos'}), 400
        try:
            airport = Airport(
                iata_code=data['iata_code'],
                airport=data['airport'],
                city=data['city'],
                state=data.get('state'),
                country=data['country'],
                latitude=data['latitude'],
                longitude=data['longitude']
            )
            db.session.add(airport)
            db.session.commit()
            return jsonify({'message': 'Airport added successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        airports = Airport.query.all()
        return jsonify([{
            'iata_code': a.iata_code,
            'airport': a.airport,
            'city': a.city,
            'state': a.state,
            'country': a.country,
            'latitude': a.latitude,
            'longitude': a.longitude
        } for a in airports])

# Agrega lógica de validación similar en `/api/flights` si es necesario.

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(host='0.0.0.0', port=port, debug=debug_mode)