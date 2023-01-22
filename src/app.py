from flask import Flask
from flask_restful import Resource, Api
from routes import routes

app = Flask(__name__)
api = Api(app)

routes.init_resources(api=api)


if __name__ == '__main__':
    app.run(debug=True)