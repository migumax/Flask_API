from flask import Flask, request
from flask_restplus import Api, Resource, fields

# tutorial source: https://towardsdatascience.com/working-with-apis-using-flask-flask-restplus-and-swagger-ui-7cf447deda7f
flask_app = Flask(__name__)
app = Api(app=flask_app,
            version="1.0",
            title="Study App: Name Recorder",
            description="A tool to manage names of app's users")

name_space = app.namespace('names', description='Manage names') # defining Swagger specs: main end-point to hit & it's description

# in order to receive/send data we should firstly specify the data model
model = app.model('Name Model',
    {'name': fields.String(required=True,
                            description="Name of the person",
                            help="Name cannot be blank")})
list_of_names = {}

@name_space.route("/<int:id>")
class MainClass(Resource):

    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
                params={'id': 'Specify the Id associated with the person'})
    
    def get(self, id):
        try:
            name = list_of_names[id]
            return {
                "status": "Person retrieved",
                "name": name
            }
        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Could not retrieve information", statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not retrieve information", statusCode="400")

    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
                params={'id': 'Specify the Id associated with the person'})
    
    @app.expect(model)
    def post(self, id):
        try:
            list_of_names[id] = request.json['name']
            return {
                    "status": "New person added",
                    "name": list_of_names[id]
                    }
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")
