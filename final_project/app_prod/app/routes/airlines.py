# app/routes/airlines.py

from flask import Blueprint, request, jsonify, Response
from flasgger import swag_from
from app import db
from app.models import Airline
import csv
import io

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
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        airlines = Airline.query.all()
        return jsonify([{'iata_code': a.iata_code, 'airline': a.airline} for a in airlines])

@airlines_bp.route('/download', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Descarga de aerolíneas en formato CSV',
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
    'tags': ['Aerolíneas']
})
def download_airlines():
    try:
        # Consultar todas las aerolíneas
        airlines = Airline.query.all()

        # Crear un objeto StringIO para escribir el CSV en memoria
        si = io.StringIO()
        cw = csv.writer(si)

        # Escribir la cabecera del CSV
        cw.writerow(['IATA Code', 'Airline'])

        # Escribir los datos de aerolíneas
        for airline in airlines:
            cw.writerow([airline.iata_code, airline.airline])

        # Obtener el contenido del CSV
        output = si.getvalue()
        si.close()

        # Crear una respuesta con el contenido del CSV
        return Response(
            output,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=airlines.csv'}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500