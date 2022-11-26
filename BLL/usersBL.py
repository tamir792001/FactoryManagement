from DAL.factoryDB_DAL import FactoryDB_DAL

class UsersBL:
    def __init__(self):
        self.__factory_db_dal = FactoryDB_DAL()

    def get_all_users(self):
        all_users = self.__factory_db_dal.get_all_users()
        return all_users

    def get_user(self, id):
        user = self.__factory_db_dal.get_user(id)
        return user

 