# app/routes/airports.py

from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app import db
from app.models import Airport

airports_bp = Blueprint('airports', __name__)

@airports_bp.route('', methods=['GET', 'POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'Lista de aeropuertos',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'iata_code': {'type': 'string'},
                        'airport': {'type': 'string'},
                        'city': {'type': 'string'},
                        'state': {'type': 'string'},
                        'country': {'type': 'string'},
                        'latitude': {'type': 'number'},
                        'longitude': {'type': 'number'}
                    }
                }
            }
        },
        201: {
            'description': 'Aeropuerto agregado exitosamente',
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
                    'iata_code': {'type': 'string'},
                    'airport': {'type': 'string'},
                    'city': {'type': 'string'},
                    'state': {'type': 'string'},
                    'country': {'type': 'string'},
                    'latitude': {'type': 'number'},
                    'longitude': {'type': 'number'}
                }
            }
        }
    ],
    'tags': ['Aeropuertos']
})
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
