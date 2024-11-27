# app/routes/airlines.py

from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app import db
from app.models import Airline

airlines_bp = Blueprint('airlines', __name__)

@airlines_bp.route('', methods=['GET', 'POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'Lista de aerolíneas',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'iata_code': {'type': 'string'},
                        'airline': {'type': 'string'}
                    }
                }
            }
        },
        201: {
            'description': 'Aerolínea agregada exitosamente',
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
                    'airline': {'type': 'string'}
                }
            }
        }
    ],
    'tags': ['Aerolíneas']
})
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
