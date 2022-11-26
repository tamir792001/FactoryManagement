from flask import Flask
from flask import Response
from bson import ObjectId
import json
from datetime import datetime
from flask_cors import CORS
from routers.departments_router import departments
from routers.auth_router import auth
from routers.employees_router import employees_bp
from routers.shifts_router import shifts_bp
from routers.users_router import users_bp


class JSONEncoder(json.JSONEncoder):
    def default(self, obj) :
        if isinstance(obj, (ObjectId, datetime)):
            return str(obj)
        return json.JSONEncoder.default(self,obj)

app = Flask(__name__)

app.json_encoder = JSONEncoder
app.url_map.strict_slashes = False
CORS(app)

app.register_blueprint(departments, url_prefix='/departments')
app.register_blueprint(employees_bp, url_prefix='/employees')
app.register_blueprint(shifts_bp, url_prefix="/shifts")
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(auth, url_prefix="/auth")

app.run()