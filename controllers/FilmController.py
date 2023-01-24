from DBEngine import engine, Session
from model.FilmDefinitions import Film, Film, Staff

local_session = Session(bind=engine)

def AddFilm(name, description, release_date):
    """Add film to the films table"""
    try:
        newFilm = Film(name, description, release_date)
        local_session.add(newFilm)
        local_session.commit()
        return True
    except:
        return False

def RemoveFilm(name):
    """Remove film from the films table"""
    try:
        query = local_session.query(Film).filter(Film.name == name)
        count = query.count()
        query.delete()
        local_session.commit()
        return count
    except:
        return -1
        
def RemoveFilmID(id):
    """Remove film from the films table using id"""
    try:
        query = local_session.query(Film).filter(Film.id == id)
        count = query.count()
        query.delete()
        local_session.commit()
        return count
    except:
        return -1

def ClearAll():
    """Remove all films from the films table"""
    try:
        query = local_session.query(Film)
        query.delete()
        local_session.commit()
        return True
    except:
        return False

def GetID(name):
    """Get film id from its name"""
    try:
        allFilm = local_session.query(Film).filter(Film.name == name)
        if not(allFilm):
            return []
        else:
            return allFilm.all()
    except:
        return -1

def GetStaff(id):
    """Get all staff that worked on this film"""
    try:
        film = local_session.query(Film).get(id)
        staff = local_session.query(Staff).filter(Staff.Film_credited.any(id=film.id))
        if staff.count() == 0:
            return []
        else:
            return staff.all()
    except:
        return -1