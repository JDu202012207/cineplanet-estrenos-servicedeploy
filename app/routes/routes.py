from flask import Blueprint, request, jsonify
import requests
import json

from flask_cors import CORS
from flasgger.utils import swag_from

routes = Blueprint('routes', __name__)

CORS(routes)


def get_cinemas():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data['cines']


def find_nearest_cinemas(user_location, number_of_cinemas=3):
    cinemas = get_cinemas()
    destinations = '|'.join([cinema['location'] for cinema in cinemas])

    # Llama a la Distance Matrix API
    api_key = "AIzaSyCrtuZ3UjtvoissX-nqT9DIZRSrc6FvlE4"  # Usa tu API Key real aquí
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        'origins': user_location,
        'destinations': destinations,
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()
        distances = results['rows'][0]['elements']
        sorted_cinemas = sorted(zip(cinemas, distances), key=lambda x: x[1]['distance']['value'])
        return sorted_cinemas[:number_of_cinemas]
    else:
        return None


@routes.route('/find_nearest_cinemas', methods=['POST'])
@swag_from('./docs/find_nearest_cinemas.yaml')
def find_nearest_cinemas_route():
    user_location = request.json.get('user_location')
    nearest_cinemas = find_nearest_cinemas(user_location, 3)  # Obtener los tres cines más cercanos
    if nearest_cinemas:
        results = [{
            'cinema': cinema['nombre'],
            'distrito': cinema['distrito'],
            'distance': distance['distance']['text'],
            'duration': distance['duration']['text']
        } for cinema, distance in nearest_cinemas]
        return jsonify(results), 200
    else:
        return jsonify({"error": "No se pudieron encontrar cines cercanos"}), 400


def calculate_route(origin, destination):
    api_key = "AIzaSyCrtuZ3UjtvoissX-nqT9DIZRSrc6FvlE4"
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        'origin': origin,
        'destination': destination,
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
