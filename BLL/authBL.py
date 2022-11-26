import jwt
from DAL.user_webservice_DAL import Users_WSDAL
class Auth_BL:
    def __init__(self):
        self.__key = "secret server key"
        self.__algorithm = "HS256"

    def __check_user_existance(self, username, email):
        users_ws_dal = Users_WSDAL()
        user_data = users_ws_dal.get_ws_user(username, email)
        if len(user_data) > 0:
            return user_data[0]
        else:
            return None

    def get_token(self, username, email):
        token = None
        user_data = self.__check_user_existance(username, email)
        if user_data is not None:
            payload =   {
                            "userID" : user_data["id"],
                            "username" : username,
                            "email" : email
                        }
            token = jwt.encode(payload, self.__key, self.__algorithm)
        return token, user_data

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.__key, self.__algorithm)
        except:
            return False
        else:
            user_data = self.__check_user_existance(payload["username"], payload["email"])
            if user_data is not None:
                return True
            else:
                return False
        #verify against db or api
    