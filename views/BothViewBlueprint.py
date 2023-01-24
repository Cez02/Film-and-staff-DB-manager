from flask import Blueprint, abort, request
from controllers.HttpHelperFunctions import CheckData
import controllers.BothController as BothController

both_page = Blueprint('both_page', __name__)

@both_page.route("/Both/addstaff", methods=['POST'])
def AddStaff():
    dict = request.args.to_dict()
    if not dict['staffid'] or not dict['filmid']:
        abort(400)
    if BothController.AddStaff(dict['staffid'], dict['filmid']):
        return "Staff added to film."
    else:
        abort(500)

@both_page.route("/Both/removestaff", methods=['DELETE'])
def RemoveStaff():
    dict = request.args.to_dict()
    if not dict['staffid'] or not dict['filmid']:
        abort(400)
    if BothController.RemoveStaff(dict['staffid'], dict['filmid']):
        return "Staff removed from film."
    else:
        abort(500)