from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from feature_engineering import routes, models
from settings import DATABASE_URL




app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
models.db.init_app(app=app)
routes.init_resources(api=api)

with app.app_context():
    models.db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
    
    
