from flask import request, abort

def CheckData(data_name):
    if not request.form[data_name]:
        abort(400)
    else:
        return request.form[data_name]
