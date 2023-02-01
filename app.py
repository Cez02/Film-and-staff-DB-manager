from flask import Flask
from controllers.StaffViewBlueprint import staff_page
from controllers.FilmViewBlueprint import film_page
from controllers.BothViewBlueprint import both_page

app = Flask(__name__)

app.register_blueprint(staff_page)
app.register_blueprint(film_page)

app.register_blueprint(both_page)