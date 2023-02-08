from flask import request
from flask_restful import Resource, Api
from flask_restful import reqparse
from .logic import LogicFactory
from .transform import PandasTransform
import logging


class FeatureEngineering(Resource):
    def __init__(self) -> None:
        self.logger = logging.getLogger(FeatureEngineering.__name__)
        super().__init__()

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("data", type=dict, action="append")
            parser.add_argument("dbtype", type=str)
            data = parser.parse_args()

            feature_data = data.get("data")
            feature_logic = (
                LogicFactory()
                .get_logic(dbtype=data.get("dbtype", "feature"))
                .save_fl(feature_data)
            )

            return {"message": feature_logic}
        except:
            return {"error": "failed"}

    def get(self):
        try:
            data = (
                LogicFactory()
                .get_logic(dbtype="dynamic_feature")
                .get_fl(PandasTransform())
            )
            return data
        except:
            raise ""


def init_resources(api: Api):
    api.add_resource(FeatureEngineering, "/feature_engineering")
