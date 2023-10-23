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

def submit_report(db, function, error, user = None):
    id = len(list(db.collection('reports').list_documents()))
    doc = db.collection('reports').document(str(id))
    if user:
        contents = {
            'timestamp': datetime.now(),
            'user_id': user.id,
            'user_name': user.name,
            'function': function,
            'error': error
        }
    else:
        contents = {
            'timestamp': datetime.now(),
            'function': function,
            'error': error
        }
    doc.set(contents)