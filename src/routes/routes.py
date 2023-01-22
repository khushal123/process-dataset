from flask_restful import Resource, Api

class FeatureEngineering(Resource):
    def get(self):
        return { 
            "Hello": "World"
        }

    def post(self):
        return {
            "Hello": "World"
        }
    


def init_resources(api: Api):
    api.add_resource(FeatureEngineering, "/")