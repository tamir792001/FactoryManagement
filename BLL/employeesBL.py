from DAL.factoryDB_DAL import FactoryDB_DAL

class EmployeesBL:
    def __init__(self):
        self.__factory_db_dal = FactoryDB_DAL()

    def get_all_employees(self):
        all_employees_list = self.__factory_db_dal.get_all_employees()
        for emp in all_employees_list:

            #Extracting the specific related department doc
            d = self.__factory_db_dal.get_department(emp["departmentID"])
            emp["departmentName"] = d["name"]

            #Extracting the specific related assignment docs, and turning them to shift docs
            emp_assignments = self.get_all_related_shifts(emp["employeeID"])
            emp_shifts = []
            if len(emp_assignments) > 0:
                emp_shifts = list(map(lambda a : self.__factory_db_dal.get_shift_doc(a["shiftID"]) ,emp_assignments))
            emp["relatedShifts"] = emp_shifts
        print("hi")
            
        return all_employees_list

    def get_employee(self, id):
        employee = self.__factory_db_dal.get_employee(id)
        return employee

    def get_all_related_shifts(self, id):
        all_assignments = self.__factory_db_dal.get_all_assignments()
        given_emp_assignments = list(filter(lambda a : id in a["employeesList"],all_assignments))
        return given_emp_assignments
        
    def validate_employee_obj(self, obj, method):
        if method == "POST":
            emp_with_same_id = self.__factory_db_dal.get_employee(int(obj["employeeID"]))
            if emp_with_same_id != None:
                return -2

        if obj.get("departmentID") != None:
            return 1
            
        if obj.get("department") != None:
            if obj["department"].isnumeric():
                department_data = self.__factory_db_dal.get_department(int(obj["department"]))
                if department_data != None:
                    obj["departmentID"] = int(obj["department"])
                    obj.pop("department")
                    return 1
            else:
                department_data = self.__factory_db_dal.get_department_by_name(obj["department"])
                if department_data != None:
                    obj["departmentID"] = department_data["departmentID"]
                    obj.pop("department")
                    return 1
        return -1

    def create_employee(self, obj):
        status = self.validate_employee_obj(obj, "POST")
        if status == 1:
            status = self.__factory_db_dal.create_employee_doc(obj)
        return status

    def update_employee(self, id, obj):
        status = self.validate_employee_obj(obj, "PUT")
        if status == 1:
            status = self.__factory_db_dal.update_employee_doc(id, obj)
        return status
        

    def delete_employee(self, id):
        all_departments = self.__factory_db_dal.get_all_departments()
        departments_that_emp_manage = list(filter(lambda d : d["manager"] == id,all_departments))
        if len(departments_that_emp_manage) > 0:
            for d in departments_that_emp_manage:
                d["manager"] = -1
                resp = self.__factory_db_dal.update_department_doc(d["departmentID"], d)
        #deleting employees shift data from assignments colletion
        emp_related_shifts = self.get_all_related_shifts(id)
        for s in emp_related_shifts:
            a = self.__factory_db_dal.get_assignment_doc(s["shiftID"])
            a_employeesList = a["employeesList"]
            a_employeesList.remove(id)
            obj = {"shiftID" : s["shiftID"], "employeesList" : a_employeesList}
            self.__factory_db_dal.update_assignment(s["shiftID"],obj)
        status = self.__factory_db_dal.delete_employee_doc(id)
        return status