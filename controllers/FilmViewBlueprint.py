from flask import Blueprint, abort, jsonify
from services.HttpHelperFunctions import CheckData
import services.FilmController as FilmController

film_page = Blueprint('film_page', __name__)

@film_page.route("/Film/add", methods=['POST'])
def AddFilm():
    name = CheckData("name")
    description = CheckData("description")
    release_date = CheckData("release_date")
    if FilmController.AddFilm(name, description, release_date):
        return "Film added"
    else:
        abort(500)

@film_page.route("/Film/remove", methods=['DELETE'])
def RemoveFilm():
    name = CheckData("name")
    res = FilmController.RemoveFilm(name)
    if res >= 0:
        return f"Removed {res} films."
    else:
        abort(500)

@film_page.route("/Film/removeid", methods=['DELETE'])
def RemoveFilmID():
    id = CheckData("id")
    res = FilmController.RemoveFilmID(id)
    if res >= 0:
        return f"Removed {res} films."
    else:
        abort(500)

@film_page.route("/Film/getall", methods=['GET'])
def GetAll():
    res = FilmController.GetAll()
    if res is int:
        abort(500)
    else:
        return [x.toDict() for x in res]

@film_page.route("/Film/clear", methods=['DELETE'])
def ClearAll():
    if FilmController.ClearAll():
        return "Films removed"
    else:
        abort(500)

@film_page.route("/Film/<name>", methods=['GET'])
def GetID(name):
    res = FilmController.GetID(name)
    if res is int:
        abort(500)
    else:
        return [x.toDict() for x in res]

@film_page.route("/Film/staff/<id>", methods=['GET'])
def GetStaff(id):
    res = FilmController.GetStaff(id)
    if res is int:
        abort(500)
    else:
        return [x.toDict() for x in res]

