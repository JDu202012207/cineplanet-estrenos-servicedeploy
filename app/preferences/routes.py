from flask import Blueprint, request, jsonify
import json
import requests
from flask_cors import CORS
from flasgger.utils import swag_from

preferences = Blueprint('preferences', __name__)

CORS(preferences)




def load_data():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data


data = load_data()


def find_cinema_by_preferences(preferences):
    if not preferences:
        return None  # Regresa None si las preferencias no están definidas
    for cinema in data['cines']:
        if cinema['nombre'] == preferences.get('nombre') and cinema['distrito'] == preferences.get('distrito'):
            return cinema
    return None


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
        return {"error": "Failed to fetch directions"}


try:
    with open('data.json', 'r') as file:
        data = json.load(file)
except Exception as e:
    print("Failed to load data:", e)
    data = {"usuarios": []}  # Proporcionar una estructura de datos predeterminada en caso de error


@swag_from('docs/get_preferences_by_dni.yaml')
@preferences.route('/get_preferences_by_dni', methods=['POST'])
def get_preferences_by_dni():
    dni = request.json.get('dni')
    if not dni:  # Verificar que el DNI ha sido proporcionado en la solicitud
        return jsonify({"error": "No DNI provided"}), 400

    # Buscar en la lista de usuarios cargada
    for item in data.get('usuarios', []):  # Uso seguro con .get para evitar KeyError si 'usuarios' no existe
        if item.get('dni') == dni:
            return jsonify(item.get('preferences', {})), 200

    return jsonify({"error": "No preferences found for the given DNI"}), 404


@swag_from('docs/save_preferences_by_dni.yaml')
@preferences.route('/find_preferred_cinema', methods=['POST'])
def find_preferred_cinema():
    user_location = request.json.get('user_location')  # Asegúrate de que el frontend envía esto
    user_preferences = request.json.get('preferences')

    preferred_cinema = find_cinema_by_preferences(user_preferences)
    if preferred_cinema:
        route = calculate_route(user_location, preferred_cinema['location'])
        if route:
            return jsonify({"cinema": preferred_cinema, "route": route}), 200
        else:
            return jsonify({"error": "No se pudo calcular la ruta"}), 400
    else:
        return jsonify({"error": "No cinema found matching the preferences"}), 404
