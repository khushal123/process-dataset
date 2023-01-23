from flask import request
from flask_restful import Resource, Api
from flask_restful import reqparse
from feature_engineering.logic import FeatureLogic

import logging



class FeatureEngineering(Resource):

    def __init__(self) -> None:
        self.logger = logging.getLogger(FeatureEngineering.__name__)
        
        super().__init__()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("data", type=dict, action="append")
        data = parser.parse_args()
        feature_data = data.get("data")
        feature_logic = FeatureLogic._save(feature_data)
        return {
            "message": feature_logic
        }


    def get(self):
        records = FeatureLogic._get()
        return {
            "calculated": records
        }


    


def init_resources(api: Api):
    api.add_resource(FeatureEngineering, "/feature_engineering")