from .models import db
import traceback

# commit eine ganze Iterable in DB
def commitAllToDB(data):
    try:
        db.session.add_all(data)
        db.session.commit()
    except Exception:
        print(traceback.format_exc())
        db.session.rollback()

def commitToDB(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception:
        print(traceback.format_exc())
        db.session.rollback()
        
def deleteFromDB(data):
    try:
        for d in data:
            db.session.delete(d)
        db.session.commit()
    except Exception:
        print(traceback.format_exc())
        db.session.rollback()