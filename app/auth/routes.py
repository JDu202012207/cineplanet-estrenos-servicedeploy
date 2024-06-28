from flask import Blueprint, request, jsonify

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    # Aquí iría tu lógica de autenticación
    return jsonify({"status": "success", "message": "Logged in successfully"})
