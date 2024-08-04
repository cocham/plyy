import database as db

def extract_user(email):
    u_id = db.get_query('SELECT id FROM USER WHERE email = ?', (email,),mul=False)

    return u_id['id'] if u_id else None
