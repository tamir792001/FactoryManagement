import requests

class Users_WSDAL:
    def __init__(self):
        self.__url = "https://jsonplaceholder.typicode.com/users"

    def get_all_ws_users(self):
        resp = requests.get(self.__url)
        return resp.json()

    #maybe this code should be in a bl
    def get_ws_user(self, username, email):
        resp = requests.get(self.__url, params={"username" : username, "email" : email}) 
        return resp.json() #this is list