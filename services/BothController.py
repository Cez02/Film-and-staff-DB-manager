from DBEngine import engine, Session
from model.FilmDefinitions import Film, Film, Staff

local_session = Session(bind=engine)

def AddStaff(staff_id, film_id):
    try:
        film = local_session.query(Film).get(film_id)
        staff = local_session.query(Staff).get(staff_id)
        if not(film) or not(staff):
            return False
        film.staff_credited.append(staff)
        local_session.commit()
        return True
    except:
        return False

def RemoveStaff(staff_id, film_id):
    try:
        film = local_session.query(Film).get(film_id)
        staff = local_session.query(Staff).get(staff_id)
        if not(film) or not(staff):
            return False
        film.staff_credited.remove(staff)
        local_session.commit()
        return True
    except:
        return False