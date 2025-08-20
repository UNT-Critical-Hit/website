import os
from datetime import datetime

DEBUG = int(os.environ.get("DEBUG", 0))


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
        username = ""
        if user.username:
            username = user.username
        else:
            username = user.name
        contents = {
            'timestamp': datetime.now(),
            'user_id': user.id,
            'user_name': username,
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

if DEBUG:
    logged_in = lambda x, y: None
    submit_report = lambda x, y, z, a = None: None