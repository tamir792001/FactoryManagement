import os, json
from DAL.factoryDB_DAL import FactoryDB_DAL
from datetime import datetime

class LogServices:
    def __init__(self):
        self.__factory_db_dal = FactoryDB_DAL()
        self.__path = os.path.join(os.getcwd(), "log")
        self.__file_path = os.path.join(self.__path, "log.json")

    #checking whether log.json's PATH already exist, if necessery, it creates it.
    def establish_log_file(self):
        if not os.path.exists(self.__path):
            os.mkdir(os.path.join(os.getcwd(),'log'))
        if not os.path.exists(self.__file_path):
            with open(self.__file_path,"w") as f:  
                initialObj = {"actions" : []}
                json.dump(initialObj,f)
        
    def log_user_actions(self, obj):

        self.establish_log_file()

        #reading data from 'log.json' file
        f = open(self.__file_path,"r")
        data = json.load(f)
        f.close()

        user_data = self.inc_user_actions(self.__factory_db_dal.get_user(obj["id"]))

        if not self.does_reach_maxActions(user_data):
            with open(self.__file_path, "w") as f:
                obj["maxActions"] = user_data["MaxActions"]
                obj["actionsMade"] = user_data["actionsMade"]
                obj["date"] = str(user_data["lastConnection"])
                data["actions"].append(obj)
                json.dump(data,f)
            return True
        return False
        
    def does_reach_maxActions(self, userObj):
        print(userObj["actionsMade"])
        if userObj["actionsMade"] >= userObj["MaxActions"]:
            print("user passes his limit of acton")
            return True   
        return False

    def inc_user_actions(self , userObj):
        self.check_user_lastConnection(userObj)
        self.__factory_db_dal.inc_user_actions(userObj["userID"])
        print(userObj)
        return self.__factory_db_dal.get_user(userObj['userID'])

    def check_user_lastConnection(self, userObj):
        today = datetime.today()
        #checks if user has connected once, if not, the db will be updated accordingly 
        if userObj.get("lastConnection"):
        #compare only the yyyy/mm/dd part of datetime obj,
        #if current date of connection bigger than last date of connection -
        # db fields of 'lastConnection & 'actionsMade resets 
            if userObj["lastConnection"].date() < today.date():
                print(userObj["lastConnection"])
                userObj["lastConnection"] = today
                userObj["actionsMade"] = 0
                self.__factory_db_dal.update_user(userObj["userID"], userObj)

        else:
            print(f"user {userObj['userID']} has made his first connection")
            self.__factory_db_dal.first_user_connection(userObj["userID"], today)



        

