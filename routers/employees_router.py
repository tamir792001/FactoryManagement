from flask import Blueprint,jsonify,request,make_response
from BLL.employeesBL import EmployeesBL
from BLL.authBL import Auth_BL
from services.actions import LogServices
import json

employees_bl = EmployeesBL()

employees_bp = Blueprint('employees' , __name__)
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

@employees_bp.route('/' , methods=['GET'])
@check_client_request
def get_all_employees():
    employees = employees_bl.get_all_employees()
    fname = request.args.get("fname")
    lname = request.args.get("lname")
    emp_current_department_ID = request.args.get("empDepartmentID")
    if fname and lname and emp_current_department_ID:
        emp = list(filter(lambda x : x["Fname"] == fname and x["Lname"] == lname and x["departmentID"] == int(emp_current_department_ID),employees))
        return jsonify(emp[0])      
    else:
        return jsonify(employees)
        


@employees_bp.route('/<string:id>' , methods=['GET'])
@check_client_request
def get_employee(id):
    employee = employees_bl.get_employee(int(id))
    return jsonify(employee)



@employees_bp.route('/', methods=['POST'])
@check_client_request
def create_employee():
    employee_data = request.json
    status = employees_bl.create_employee(employee_data)
    if status == -1:
        return make_response(jsonify({"status" : "Given Department Does Not Exist"}), 404)
    elif status == -2:
        return make_response(jsonify({"status" : "Given Employee ID Already Exist"}), 404)
    return make_response(jsonify({"status" : status}) , 201)

@employees_bp.route('/<string:id>' , methods=['PUT'])
@check_client_request
def update_employee(id):
    data = request.json
    status = employees_bl.update_employee(int(id), data)
    if status == -1:
        return make_response(jsonify({"status" : "Given Department Does Not Exist"}), 404)
    return make_response(jsonify({"status" : status}) , 200)

@employees_bp.route('/' , methods=['PUT'])
@check_client_request
def update_employee_by_agrs():
    fname = request.args.get("fname")
    lname = request.args.get("lname")
    emp_current_department_ID = int(request.args.get("empDepartmentID"))
    all_emp = employees_bl.get_all_employees()
    emp = list(filter(lambda x : x["Fname"] == fname and x["Lname"] == lname and x["departmentID"] == emp_current_department_ID,all_emp))
    data = request.json
    status = employees_bl.update_employee(int(emp[0]["employeeID"]), data)
    return make_response(jsonify({"status" : status}), 200)

@employees_bp.route('/<string:id>' , methods=['DELETE'])
@check_client_request
def delete_employee(id):
    status = employees_bl.delete_employee(int(id))
    return jsonify(status)