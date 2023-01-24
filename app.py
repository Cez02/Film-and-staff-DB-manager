from flask import Flask
from views.StaffViewBlueprint import staff_page
from views.FilmViewBlueprint import film_page
from views.BothViewBlueprint import both_page
import controllers.StaffController as StaffController

app = Flask(__name__)

app.register_blueprint(staff_page)
app.register_blueprint(film_page)

app.register_blueprint(both_page)