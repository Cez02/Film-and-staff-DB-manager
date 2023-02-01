from flask import Blueprint, abort, request
from services.HttpHelperFunctions import CheckData
import services.StaffController as StaffController

staff_page = Blueprint('staff_page', __name__)

@staff_page.route("/Staff/add", methods=['POST'])
def AddStaff():
    first_name = CheckData("first_name")
    last_name = CheckData("last_name")
    speciality = CheckData("speciality")
    if StaffController.AddStaff(first_name, last_name, speciality):
        return "Staff added"
    else:
        abort(500)

@staff_page.route("/Staff/remove", methods=['DELETE'])
def RemoveStaff():
    first_name = CheckData("first_name")
    last_name = CheckData("last_name")

    res = StaffController.RemoveStaff(first_name, last_name)
    if res >= 0:
        return f"Removed {res} staff."
    else:
        abort(500)

@staff_page.route("/Staff/removeid", methods=['DELETE'])
def RemoveStaffID():
    id = CheckData("id")
    res = StaffController.RemoveStaffID(id)
    if res >= 0:
        return f"Removed {res} staff."
    else:
        abort(500)

@staff_page.route("/Staff/clear", methods=['DELETE'])
def ClearAll():
    if StaffController.ClearAll():
        return "Staff removed"
    else:
        abort(500)

@staff_page.route("/Staff", methods=['GET'])
def GetID():
    dict = request.args.to_dict()
    if not dict['first_name'] or not dict['last_name']:
        abort(400)
    res = StaffController.GetID(dict['first_name'], dict['last_name'])
    if res is int:
        abort(500)
    else:
        return [x.toDict() for x in res]

@staff_page.route("/Staff/film/<id>", methods=['GET'])
def GetFilms(id):
    res = StaffController.GetFilms(id)
    if res is int:
        abort(500)
    else:
        return [x.toDict() for x in res]

