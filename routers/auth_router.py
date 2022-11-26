from flask import Blueprint,jsonify,make_response,request
from BLL.authBL import Auth_BL

auth = Blueprint("auth" , __name__)

@auth.route("/login", methods=['POST'])
def login():
    auth_bl = Auth_BL()
    user_input = request.json
    token, user_data = auth_bl.get_token(user_input["username"], user_input["email"])
    if token is not None:
        return make_response({"accesstoken" : token, "name" : user_data["name"], "userID" : user_data["id"] },200)
    else:
        return make_response({"error" : "UNAUTHENTICATED"},401)

