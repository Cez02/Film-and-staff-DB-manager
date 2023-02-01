import requests
from http import HTTPStatus
import ast

ServerURL = "http://127.0.0.1:5000"

def AddStaff(*args):
    """Add staff with args: <first name> <last name> <speciality>"""
    try:
        form_data = {
            "first_name" : args[0],
            "last_name" : args[1],
            "speciality" : args[2]
        }
        res = requests.post(ServerURL + "/Staff/add", data=form_data)
        if res.status_code == HTTPStatus.OK:
            return True
        else:
            raise Exception(f"Failed to add staff with response status code: {res.status_code}")
    except Exception as e:
        raise e

def GetAllStaff(*args):
    """Get all staff"""
    try:
        res = requests.get(ServerURL + "/Staff/getall")
        if res.status_code == HTTPStatus.OK:
            return ast.literal_eval(res.text)
        else:
            raise Exception(f"Failed to add staff with response status code: {res.status_code}")
    except Exception as e:
        raise e

def UpdateStaff(*args):
    """Get all staff"""
    try:
        print(args)
        if len(args[1]) == 0 or len(args[2]) == 0 or len(args[3]) == 0:
            raise Exception(f"Record field must be non-null.")

        form_data = {
            "id" : args[0],
            "first_name" : args[1],
            "last_name" : args[2],
            "speciality" : args[3]
        }
        res = requests.put(ServerURL + "/Staff/update", data=form_data)
        if res.status_code == HTTPStatus.OK:
            return True
        else:
            raise Exception(f"Failed to update staff with response status code: {res.status_code}")
    except Exception as e:
        raise e

def RemoveStaffByID(*args):
    """Remove staff with args: <staff id>"""
    try:
        form_data = {
            "id" : args[0],
        }
        res = requests.delete(ServerURL + "/Staff/removeid", data=form_data)
        if res.status_code == HTTPStatus.OK:
            return True
        else:
            raise Exception(f"Failed to remove staff with response status code: {res.status_code}")
    except Exception as e:
        raise e

def AddFilmToStaff(args):
    """Add film to staff: <staff id> <film id>"""
    try:
        res = requests.delete(ServerURL + f"/Both/removestaff?staffid={args[0]}&filmid={args[1]}")
        if res.status_code == HTTPStatus.OK:
            return True
        else:
            raise Exception(f"Failed to add staff to film: {res.status_code}")
    except Exception as e:
        raise e