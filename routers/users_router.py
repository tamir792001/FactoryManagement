from flask import Blueprint,make_response,jsonify,request
from BLL.usersBL import UsersBL
from BLL.authBL import Auth_BL
from services.actions import LogServices
import json

users_bp = Blueprint('users' , __name__)

users_bl = UsersBL()
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


@users_bp.route('/', methods=['GET'])
@check_client_request
def get_all_users():
    all_users = users_bl.get_all_users()
    return jsonify(all_users)

@users_bp.route("/<string:id>" , methods=['GET'])
def get_user(id):
    user = users_bl.get_user(int(id))
    return jsonify(user)