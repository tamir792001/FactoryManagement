from DAL.factoryDB_DAL import FactoryDB_DAL

class ShiftsBL:
    def __init__(self):
        self.__factory_db_dal = FactoryDB_DAL()

    def get_all_shifts(self):
        all_shifts = self.__factory_db_dal.get_all_shifts()
        return all_shifts
    
    def get_shift(self, id):
        shift = self.__factory_db_dal.get_shift_doc(id)
        return shift

    def validate_obj(self, obj):
        all_shifts = self.__factory_db_dal.get_all_shifts()
        same_id_shift = list(filter(lambda s : s["shiftID"] == obj["shiftID"],all_shifts))
        if len(same_id_shift) > 0:
            return False
        return True

    def create_shift(self, obj):
        if not self.validate_obj(obj):
            return -1
        assignment_obj = {"shiftID" : obj["shiftID"], "employeesList" : []}
        assign_status = self.__factory_db_dal.create_assignment_doc(assignment_obj)
        status = self.__factory_db_dal.create_shift_doc(obj)
        return status

    def update_shift(self, id, obj):
        status = self.__factory_db_dal.update_shift_doc(id, obj)
        return status

    def update_assignment(self, shift_id, emp_id):
        given_assignment = self.__factory_db_dal.get_assignment_doc(shift_id)
        if emp_id in given_assignment["employeesList"]:
            return -2
        if len(given_assignment["employeesList"]) == 2:
            return -1
        else:
            given_assignment["employeesList"].append(emp_id)
        obj = {"shiftID" : shift_id, "employeesList" : given_assignment["employeesList"]}
        status = self.__factory_db_dal.update_assignment(shift_id, obj)
        return status

