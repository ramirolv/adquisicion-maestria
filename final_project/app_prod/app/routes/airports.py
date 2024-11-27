# app/routes/airports.py

from flask import Blueprint, request, jsonify, Response
from flasgger import swag_from
from app import db
from app.models import Airport
import csv
import io

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
            db.session.rollback()
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

@airports_bp.route('/download', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Descarga de aeropuertos en formato CSV',
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
    'tags': ['Aeropuertos']
})
def download_airports():
    try:
        # Consultar todos los aeropuertos
        airports = Airport.query.all()

        # Crear un objeto StringIO para escribir el CSV en memoria
        si = io.StringIO()
        cw = csv.writer(si)

        # Escribir la cabecera del CSV
        cw.writerow(['IATA Code', 'Airport', 'City', 'State', 'Country', 'Latitude', 'Longitude'])

        # Escribir los datos de aeropuertos
        for airport in airports:
            cw.writerow([
                airport.iata_code,
                airport.airport,
                airport.city,
                airport.state if airport.state else '',
                airport.country,
                airport.latitude,
                airport.longitude
            ])

        # Obtener el contenido del CSV
        output = si.getvalue()
        si.close()

        # Crear una respuesta con el contenido del CSV
        return Response(
            output,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=airports.csv'}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
