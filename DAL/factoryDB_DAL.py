
from pymongo import MongoClient


class FactoryDB_DAL:
    def __init__(self):
        self.__client = MongoClient(port=27017)
        self.__db = self.__client["factoryDB"]
        self.__departments_collcetion = self.__db["departments"]
        self.__employees_collcetion = self.__db["employees"]
        self.__shifts_collection = self.__db["shifts"]
        self.__assignments_collection = self.__db["assignments"]
        self.__users_collection = self.__db["users"]

    def get_all_assignments(self):
        all_assignments = list(self.__assignments_collection.find({}))
        return all_assignments

    def get_assignment_doc(self, shift_id):
        assignment = self.__assignments_collection.find_one({"shiftID" : shift_id})
        return assignment

    def create_assignment_doc(self, obj):
        self.__assignments_collection.insert_one(obj)
        return "Assignment Created!"

    def update_assignment(self, shift_id, obj):
        self.__assignments_collection.update_one({"shiftID" : shift_id}, {"$set" : obj})
        return "Assignment Updated"
    
    def get_all_shifts(self):

        all_shifts = self.__shifts_collection.aggregate([{
                                                            "$lookup" :
                                                            {
                                                                "from" : "assignments",
                                                                "localField" : "shiftID",
                                                                "foreignField" : "shiftID",
                                                                "as" : "assignments"
                                                            }
                                                        }])
        return list(all_shifts)
    
    def get_shift_doc(self, id):
        shift_doc = self.__shifts_collection.find_one({"shiftID" : id})
        return shift_doc

    def create_shift_doc(self, obj):
        self.__shifts_collection.insert_one(obj)
        return "Shift Posted!"

    def update_shift_doc(self, id, obj):
        self.__shifts_collection.update_one({"shiftID" : id}, {"$set" : obj})
        return "Shift Updated"

    #No need
    def delete_shift_doc(self,id):
        self.__shifts_collection.delete_one({"shiftID" : id})
        return "Shift Deleted"

    def get_all_departments(self):
        all_departments = list(self.__departments_collcetion.find({}))
        return all_departments

    def get_department(self, id):
        department = self.__departments_collcetion.find_one({"departmentID" : id})
        return department
    
    def get_department_by_name(self, name):
        print(name)
        department = self.__departments_collcetion.find_one({"name" : name})
        return department

    def create_department_doc(self, obj):
        self.__departments_collcetion.insert_one(obj)
        return "department Posted!"

    def update_department_doc(self, id, obj):
        self.__departments_collcetion.update_one({"departmentID" : id} , {"$set" : obj})
        return "department Updated!"

    def delete_department_doc(self, id):
        self.__departments_collcetion.delete_one({"departmentID" : id})
        return "department Deleted"

    def get_all_employees(self):
        all_employees = list(self.__employees_collcetion.find({}))
        return all_employees

    def get_employee(self, id):
        employee = self.__employees_collcetion.find_one({"employeeID" : id})
        return employee

    def create_employee_doc(self, obj):
        self.__employees_collcetion.insert_one(obj)                                         
        return 'employee Posted'

    def update_employee_doc(self, id, obj):
        self.__employees_collcetion.update_one({"employeeID" : id}, {"$set" : obj})
        return "employee Updated!"

    def delete_employee_doc(self, id):
        self.__employees_collcetion.delete_one({"employeeID" : id})
        return "employee Deleted"

    def get_all_users(self):
        all_users = list(self.__users_collection.find({}))
        return all_users

    def get_user(self,id):
        user = self.__users_collection.find_one({"userID" : id})
        return user

    def update_user(self, id, obj):
        self.__users_collection.update_one({"userID" : id}, { "$set" : obj})
        return "User Updated"

    def inc_user_actions(self, id):
        self.__users_collection.update_one({"userID" : id}, {"$inc" : {"actionsMade" : 1}})
        return "user actions incermented"

    def first_user_connection(self, id, dateObj):
        self.__users_collection.update_one({"userID" : id}, {"$set" : {"lastConnection" : dateObj}})
        return "user first connected"


    


