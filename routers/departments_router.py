from flask import Blueprint,jsonify,request,make_response, Response
from BLL.departmentsBL import DepartmentsBL
from BLL.authBL import Auth_BL
from services.actions import LogServices
import json


departments = Blueprint("deparments", __name__)

departments_bl = DepartmentsBL()
log_services = LogServices()

def check_user(token):
    auth_bl = Auth_BL()
    return auth_bl.verify_token(token)

def check_client_request(func):
    def decorator(*args, **kwargs):
        if request.headers and request.headers.get("x-access-token") is not None:
            token = request.headers.get("x-access-token")
            if not check_user(token):
                return make_response(jsonify({"error" : "UNAUTHORIZED"}), 403)
        else:
            return make_response(jsonify({"error" : "UNAUTHENTICATED"}), 401)

        #Adding action to 'log.json' file
        user_log_data = json.loads(request.headers.get("userInformation"))
        if log_services.log_user_actions(user_log_data):
            return func(*args, **kwargs)
        return make_response(jsonify({"error" : "Reached Daily Actions Limit"}), 403)
    decorator.__name__ = func.__name__
    return decorator


@departments.route("/", methods=['GET'])
@check_client_request
def get_all_departments():
    #log user's action to 'log.json' file
    #user_log_data = json.loads(request.headers.get("userInformation"))
    #if log_services.log_user_actions(user_log_data):
    departments = departments_bl.get_all_departments()
    return jsonify(departments)
    #return make_response(jsonify({"error" : "Reached Daily Actions Limit"}), 403)



@departments.route('/edit', methods=['GET'])
@check_client_request
def get_department_with_qs():
    dname = request.args.get("dname")
    department = departments_bl.get_department_by_name(dname)
    return jsonify(department)


@departments.route("/<string:id>" , methods=['GET'])
@check_client_request
def get_department(id):
    department = departments_bl.get_department(int(id))
    return jsonify(department)

@departments.route("/", methods=['POST'])
@check_client_request
def create_department():    
    department_data = request.json
    status = departments_bl.create_department(department_data)
    if status == -1:
        status = "ID or Name already exist, Input different values"
        return make_response(jsonify({"status" : status}), 409)
    elif status == -2:
        status = "Manager does not exist"
        return make_response(jsonify({"status" : status}), 404)
    else:
        return make_response(jsonify({"status" : status}), 201)

@departments.route("/<string:id>", methods=['PUT'])
@check_client_request
def update_department(id):
    department_data = request.json
    status = departments_bl.update_department(int(id), department_data)
        
    if status == -1:
        status = "Selected department name already taken"
        return make_response(jsonify({"status" : status}), 409)
    elif status == -2:
        status = "Manager does not exist"
        return make_response(jsonify({"status" : status}), 404)
    else:
        return make_response(jsonify({"status" : status}), 200)


@departments.route("/<string:id>", methods=['DELETE'])
@check_client_request
def delete_department(id):
    status = departments_bl.delete_department(int(id))
    return jsonify(status)
