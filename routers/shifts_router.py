from BLL.shiftsBL import ShiftsBL
from flask import Blueprint, jsonify, make_response, request
from BLL.authBL import Auth_BL
from services.actions import LogServices
import json

shifts_bl = ShiftsBL()

shifts_bp = Blueprint("shifts", __name__)
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

@shifts_bp.route("/" , methods = ['GET'])
@check_client_request
def get_all_shifts():
    all_shifts = shifts_bl.get_all_shifts()
    return jsonify(all_shifts)

@shifts_bp.route('/<string:id>' , methods=['GET'])
@check_client_request
def get_shift(id):
    shift = shifts_bl.get_shift(int(id))
    return jsonify(shift)

@shifts_bp.route("/" , methods=['POST'])
@check_client_request
def create_shift():
    obj = request.json
    status = shifts_bl.create_shift(obj)
    if status == -1:
        return make_response(jsonify({"status" : "Given Shift ID Already Exist"}), 409)
    else:
        return make_response(jsonify({"status" : status}), 201)

@shifts_bp.route('/<string:id>', methods=['PUT'])
@check_client_request
def update_shift(id):
    obj = request.json
    status = shifts_bl.update_shift(int(id), obj)
    return make_response(jsonify({"status" : status}), 200)

@shifts_bp.route('/assignments' , methods=['PUT'])
@check_client_request
def update_assignment():
    shift_id = request.args.get("shiftID")
    emp_id = request.args.get("empID")
    status = shifts_bl.update_assignment(int(shift_id), int(emp_id))
    if status == -1:
        status = "Shift is fully assigned!"
        return make_response(jsonify({"status" : status}), 409)
    elif status == -2:
        status = "Given employee already assigned to selected shift!"
        return make_response(jsonify({"status" : status}), 409)
    return make_response(jsonify({"status" : status}), 200)



