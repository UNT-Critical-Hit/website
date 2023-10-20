from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app

def logged_in(id, db):
    doc = db.collection('users').document(str(id))
    contents = doc.get().to_dict()
    if not contents:
        contents = {
            'last_login': datetime.now()
        }
    else:
        contents['last_login'] = datetime.now()
    doc.set(contents)