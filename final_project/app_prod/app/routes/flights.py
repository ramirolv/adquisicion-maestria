# app/routes/flights.py

from flask import Blueprint, request, jsonify, Response, current_app, stream_with_context
from flasgger import swag_from
from app import db
from app.models import Flight
import csv
import io

flights_bp = Blueprint('flights', __name__)


@flights_bp.route('', methods=['GET', 'POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'Lista de vuelos',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'year': {'type': 'integer'},
                        'month': {'type': 'integer'},
                        'day': {'type': 'integer'},
                        'day_of_week': {'type': 'integer'},
                        'airline': {'type': 'string'},
                        'flight_number': {'type': 'string'},
                        'tail_number': {'type': 'string'},
                        'origin_airport': {'type': 'string'},
                        'destination_airport': {'type': 'string'},
                        'scheduled_departure': {'type': 'integer'},
                        'departure_time': {'type': 'integer'},
                        'departure_delay': {'type': 'integer'},
                        # Agregar otros campos según sea necesario
                    }
                }
            }
        },
        201: {
            'description': 'Vuelo agregado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Datos incompletos o inválidos'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': False,
            'schema': {
                'type': 'object',
                'properties': {
                    'year': {'type': 'integer'},
                    'month': {'type': 'integer'},
                    'day': {'type': 'integer'},
                    'day_of_week': {'type': 'integer'},
                    'airline': {'type': 'string'},
                    'flight_number': {'type': 'string'},
                    'tail_number': {'type': 'string'},
                    'origin_airport': {'type': 'string'},
                    'destination_airport': {'type': 'string'},
                    'scheduled_departure': {'type': 'integer'},
                    'departure_time': {'type': 'integer'},
                    'departure_delay': {'type': 'integer'},
                    # Agregar otros campos según sea necesario
                }
            }
        }
    ],
    'tags': ['Vuelos']
})
def handle_flights():
    if request.method == 'POST':
        data = request.get_json()
        # Validar los campos requeridos
        required_fields = ['year', 'month', 'day', 'day_of_week', 'airline', 'flight_number',
                           'origin_airport', 'destination_airport', 'scheduled_departure',
                           'departure_time', 'departure_delay']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Datos incompletos o inválidos'}), 400
        try:
            flight = Flight(
                year=data['year'],
                month=data['month'],
                day=data['day'],
                day_of_week=data['day_of_week'],
                airline=data['airline'],
                flight_number=data['flight_number'],
                tail_number=data.get('tail_number'),
                origin_airport=data['origin_airport'],
                destination_airport=data['destination_airport'],
                scheduled_departure=data['scheduled_departure'],
                departure_time=data['departure_time'],
                departure_delay=data['departure_delay'],
                taxi_out=data.get('taxi_out'),
                wheels_off=datetime.fromisoformat(data['wheels_off']) if data.get('wheels_off') else None,
                scheduled_time=data.get('scheduled_time'),
                elapsed_time=data.get('elapsed_time'),
                air_time=data.get('air_time'),
                distance=data.get('distance'),
                wheels_on=datetime.fromisoformat(data['wheels_on']) if data.get('wheels_on') else None,
                taxi_in=data.get('taxi_in'),
                scheduled_arrival=datetime.fromisoformat(data['scheduled_arrival']) if data.get('scheduled_arrival') else None,
                arrival_time=datetime.fromisoformat(data['arrival_time']) if data.get('arrival_time') else None,
                arrival_delay=data.get('arrival_delay'),
                diverted=data.get('diverted', False),
                cancelled=data.get('cancelled', False),
                cancellation_reason=data.get('cancellation_reason'),
                air_system_delay=data.get('air_system_delay'),
                security_delay=data.get('security_delay'),
                airline_delay=data.get('airline_delay'),
                late_aircraft_delay=data.get('late_aircraft_delay'),
                weather_delay=data.get('weather_delay')
            )
            db.session.add(flight)
            db.session.commit()
            return jsonify({'message': 'Flight added successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        flights = Flight.query.all()
        return jsonify([{
            'id': f.id,
            'year': f.year,
            'month': f.month,
            'day': f.day,
            'day_of_week': f.day_of_week,
            'airline': f.airline,
            'flight_number': f.flight_number,
            'tail_number': f.tail_number,
            'origin_airport': f.origin_airport,
            'destination_airport': f.destination_airport,
            'scheduled_departure': f.scheduled_departure,
            'departure_time': f.departure_time,
            'departure_delay': f.departure_delay,
            # Agregar otros campos según sea necesario
        } for f in flights])



@flights_bp.route('/download', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Descarga de vuelos en formato CSV',
            'content': {
                'text/csv': {
                    'schema': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    },
    'tags': ['Vuelos']
})
def download_flights():
    def generate():
        try:
            # Crear un objeto StringIO para el encabezado
            data = io.StringIO()
            writer = csv.writer(data)
            writer.writerow([
                'ID', 'Year', 'Month', 'Day', 'Day of Week', 'Airline', 'Flight Number',
                'Tail Number', 'Origin Airport', 'Destination Airport', 'Scheduled Departure',
                'Departure Time', 'Departure Delay', 'Taxi Out', 'Wheels Off', 'Scheduled Time',
                'Elapsed Time', 'Air Time', 'Distance', 'Wheels On', 'Taxi In',
                'Scheduled Arrival', 'Arrival Time', 'Arrival Delay', 'Diverted',
                'Cancelled', 'Cancellation Reason', 'Air System Delay', 'Security Delay',
                'Airline Delay', 'Late Aircraft Delay', 'Weather Delay'
            ])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

            # Usar yield_per para iterar en batches y evitar cargar todo en memoria
            query = Flight.query.yield_per(1000).enable_eagerloads(False)
            for flight in query:
                writer.writerow([
                    flight.id,
                    flight.year,
                    flight.month,
                    flight.day,
                    flight.day_of_week,
                    flight.airline,
                    flight.flight_number,
                    flight.tail_number if flight.tail_number else '',
                    flight.origin_airport,
                    flight.destination_airport,
                    flight.scheduled_departure,
                    flight.departure_time,
                    flight.departure_delay,
                    flight.taxi_out if flight.taxi_out is not None else '',
                    flight.wheels_off.isoformat() if flight.wheels_off else '',
                    flight.scheduled_time if flight.scheduled_time is not None else '',
                    flight.elapsed_time if flight.elapsed_time is not None else '',
                    flight.air_time if flight.air_time is not None else '',
                    flight.distance if flight.distance is not None else '',
                    flight.wheels_on.isoformat() if flight.wheels_on else '',
                    flight.taxi_in if flight.taxi_in is not None else '',
                    flight.scheduled_arrival.isoformat() if flight.scheduled_arrival else '',
                    flight.arrival_time.isoformat() if flight.arrival_time else '',
                    flight.arrival_delay if flight.arrival_delay is not None else '',
                    flight.diverted,
                    flight.cancelled,
                    flight.cancellation_reason if flight.cancellation_reason else '',
                    flight.air_system_delay if flight.air_system_delay is not None else '',
                    flight.security_delay if flight.security_delay is not None else '',
                    flight.airline_delay if flight.airline_delay is not None else '',
                    flight.late_aircraft_delay if flight.late_aircraft_delay is not None else '',
                    flight.weather_delay if flight.weather_delay is not None else ''
                ])
                yield data.getvalue()
                data.seek(0)
                data.truncate(0)
        except Exception as e:
            # Registrar el error en los logs
            current_app.logger.error(f"Error al descargar vuelos: {str(e)}")
            yield ''  # Puedes optar por no yield nada o un mensaje de error

    return Response(
        stream_with_context(generate()),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=flights.csv'}
    )