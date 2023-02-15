from flask import Flask, request
from movements import movement
from population import pop

app = Flask(__name__)
app.register_blueprint(movement)
app.register_blueprint(pop)

@app.route("/")
def hello():
    return "Hello, Trying to build a movement tracker app!"

@app.route("/name/<name>")
def get_book_name(name):
    return "name : {}".format(name)

@app.route("/details")
def get_book_details():
    author=request.args.get('author')
    published=request.args.get('published')
    return "Author : {}, Published: {}".format(author,published)

if __name__ == '__main__':
    app.run()