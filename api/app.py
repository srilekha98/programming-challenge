from flask import Flask, request
from movements import movement
from population import pop
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(movement)
app.register_blueprint(pop)
CORS(app)

@app.route("/")
def hello():
    return "Hello, Trying to build a movement tracker app!"


if __name__ == '__main__':
    app.run()