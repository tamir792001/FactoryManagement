from DAL.factoryDB_DAL import FactoryDB_DAL

class DepartmentsBL:
    def __init__(self):
        self.__factory_db_dal = FactoryDB_DAL()

    def get_all_departments(self):
        employees = self.__factory_db_dal.get_all_employees()
        departments = self.__factory_db_dal.get_all_departments()
        for d in departments:
            employees_in_d = list(filter(lambda x : x["departmentID"] == d["departmentID"], employees))
            employees_in_d_names = list(map(lambda x : x["Fname"] + " " + x["Lname"], employees_in_d))
            d["employeesList"] = employees_in_d_names
        return departments

    def get_department(self, id):
        department = self.__factory_db_dal.get_department(id)
        return department
    
    def get_department_by_name(self, dname):
        department = self.__factory_db_dal.get_department_by_name(dname)
        if department is not None:
            all_employees = self.__factory_db_dal.get_all_employees()
            employees_not_in_d = list(filter(lambda x : x["departmentID"] != department["departmentID"],all_employees))
            employees_not_in_d_names = list(map(lambda x : x["Fname"] + " " + x["Lname"], employees_not_in_d))
            department["externalEmployeesList"] = employees_not_in_d
        return department

    def create_department(self, obj):
        departments = self.get_all_departments()
        all_emps = self.__factory_db_dal.get_all_employees()

        first_creation_added_msg = ""

        #check if there are already departments with same fields in factory
        if len(departments) > 0:
            same_field_departments = list(filter(lambda x : x["name"] == obj["name"] or x["departmentID"] == obj["departmentID"] ,departments))
            if len(same_field_departments) > 0:
                return -1 

        #checks whether the inputed manager's id is linked to an existed employee in factory, else - sets it to -1
        if len(all_emps) > 0:
            emp = self.__factory_db_dal.get_employee(obj["manager"])
            if emp == None:
                return -2
        else:
            obj["manager"] = -1
            first_creation_added_msg = "\nManager ID set to -1 (no employees in factory yet)"

        status = self.__factory_db_dal.create_department_doc(obj)
        return status + first_creation_added_msg


    def update_department(self, id, obj):

        #checks if user decided to change original department name, if True -
        #checks if new given department name do not already exist
        original_d = self.get_department(id)
        if original_d["name"] != obj["name"]:
            other_d_with_same_name = self.get_department_by_name(obj["name"])
            if other_d_with_same_name is not None:
                return -1

        #checks if given manager's id alredy exist, if False: return -2
        emp = self.__factory_db_dal.get_employee(obj["manager"])
        if obj["manager"] != -1 and emp == None:
            return -2

        status = self.__factory_db_dal.update_department_doc(id, obj)
        return status

    def delete_department(self, id):
        all_emp = self.__factory_db_dal.get_all_employees()
        employees_in_d = list(filter(lambda emp : emp["departmentID"] == id ,all_emp))
        for emp in employees_in_d:
            self.__factory_db_dal.delete_employee_doc(emp["employeeID"])
            #deleting employee shifts & assignments data from assignments colletion
            all_assignments = self.__factory_db_dal.get_all_assignments()
            emp_related_shifts = list(filter(lambda a : emp["employeeID"] in a["employeesList"],all_assignments))
            for s in emp_related_shifts:
                a = self.__factory_db_dal.get_assignment_doc(s["shiftID"])
                a_employeesList = a["employeesList"]
                a_employeesList.remove(emp["employeeID"])
                obj = {"shiftID" : s["shiftID"], "employeesList" : a_employeesList}
                self.__factory_db_dal.update_assignment(s["shiftID"],obj)
        status = self.__factory_db_dal.delete_department_doc(id)
        return status