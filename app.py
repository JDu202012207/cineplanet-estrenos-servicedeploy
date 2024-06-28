from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
Swagger = Swagger(app)

# Configura CORS para permitir todas las fuentes
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
