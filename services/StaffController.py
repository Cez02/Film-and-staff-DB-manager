from DBEngine import engine, Session
from model.FilmDefinitions import Film, Staff

local_session = Session(bind=engine)

def AddStaff(first_name, last_name, speciality):
    """Add a new staff to the staff table"""
    try:
        newStaff = Staff(first_name, last_name, speciality)
        local_session.add(newStaff)
        local_session.commit()
        return True
    except:
        return False

def RemoveStaff(first_name, last_name):
    """Remove staff from the staff table"""
    try:
        query = local_session.query(Staff).filter(Staff.first_name == first_name, Staff.last_name == last_name)
        count = query.count()
        query.delete()
        local_session.commit()
        return count
    except:
        return -1
        
def RemoveStaffID(id):
    """Remove staff from the staff table using the staff id"""
    try:
        query = local_session.query(Staff).filter(Staff.id == id)
        count = query.count()
        query.delete()
        local_session.commit()
        return count
    except:
        return -1

def GetAll():
    """Get all staff"""
    try:
        allStaff = local_session.query(Staff)
        if not(allStaff):
            return []
        else:
            return allStaff.all()
    except:
        return -1

def ClearAll():
    """Remove all staff from the staff table"""
    try:
        query = local_session.query(Staff)
        query.delete()
        local_session.commit()
        return True
    except:
        return False

def GetID(first_name, last_name):
    """Get staff id from their name"""
    try:
        staff = local_session.query(Staff).filter(Staff.first_name == first_name, Staff.last_name == last_name)
        if not(staff):
            return []
        else:
            return staff.all()
    except:
        return -1

def UpdateStaff(id, first_name, last_name, speciality):
    """Get staff id from their name"""
    try:
        staff = local_session.query(Staff).get(id)
        if first_name is not None:
            staff.first_name = first_name
        if last_name is not None:
            staff.last_name = last_name
        if speciality is not None:
            staff.speciality = speciality
        
        local_session.commit()
        
        if not(staff):
            return -1
        else:
            return staff.all()
    except:
        return -1

def GetFilms(id):
    """Get all films the staff has worked on"""
    try:
        staff = local_session.query(Staff).get(id)
        allfilms = local_session.query(Film).filter(Film.staff_credited.any(id=staff.id))
        if allfilms.count() == 0:
            return []
        else:
            return allfilms.all()
    except:
        return -1