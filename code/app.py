from flask import Flask
from flask_cors import CORS
from Backend.backendService import backendApp_bp

app = Flask(__name__)
# CORS(app)

app.register_blueprint(backendApp_bp)

if __name__ == '__main__':
    app.run(debug=True)