# models.py
from uuid import uuid4
import sqlite3
import os
import database as db


def curator_info(id):
    curator_info = []
    curator_tags = []

    curator = db.get_query('SELECT * FROM CURATOR WHERE id = ?', (id,), mul=False)
    curator_info.extend([curator[i] for i in range(len(curator))])
    
    ctags = db.get_query('''
                        SELECT TAG.name
                        FROM CURATOR
                        JOIN C_TAG ON CURATOR.id = C_TAG.c_id
                        JOIN TAG ON C_TAG.t_id = TAG.id
                        WHERE CURATOR.id = ?
                        ''', (id,))

    curator_tags.extend([ctags[i]['name'] for i in range(len(ctags))])
    curator_info.append(curator_tags)
    return curator_info

def cu_plyy_tag(id, pid):
    plyy_tags = []
    
    cu_pgtag = db.get_query('''
                SELECT GENRE.name
                FROM GENRE
                JOIN PLYY ON PLYY.g_id = GENRE.id
                WHERE PLYY.c_id = ? and PLYY.id = ?
                ''', (id, pid))
    
    for pgtag in cu_pgtag:
        plyy_tags.append(pgtag['name'])
    
    cu_ptag = db.get_query('''    
            SELECT tag.name
            FROM PLYY
            JOIN P_TAG ON PLYY.id = P_TAG.p_id
            JOIN TAG ON P_TAG.t_id = TAG.id
            WHERE PLYY.c_id = ? and PLYY.id = ?''', (id, pid))

    for t in cu_ptag:
        plyy_tags.append(t['name'])

    return plyy_tags

def cu_plyy(id):
    plyy_list = []

    plyy = db.get_query('SELECT * FROM PLYY WHERE c_id = ?', (id,))

    for p in plyy:  # 플리 객체
        each_plyy = [p[i] for i in range(len(p))]
        each_plyy.append(cu_plyy_tag(id, each_plyy[0]))
        plyy_list.append(each_plyy)

    return plyy_list

def curatorlike_status(c_id, u_id):

    likes = db.get_query('SELECT * FROM C_LIKE WHERE c_id = ? and u_id = ?', (c_id, u_id),mul=False)

    return bool(likes)

def curator_like(c_id, u_id):
    try:
        row = db.get_query('SELECT * FROM C_LIKE WHERE u_id = ? AND c_id = ?', (u_id,c_id),mul=False)
        if not row:
            db.execute_query('INSERT INTO C_LIKE (u_id, c_id) VALUES (?, ?)', (u_id, c_id))
        return True
    except Exception as e:
        print(f"Error inserting like: {e}")
        db.roll()
        return False

def curator_unlike(c_id, u_id):
    try:
        row = db.get_query('SELECT * FROM C_LIKE WHERE u_id = ? AND c_id = ?', (u_id, c_id),mul=False)
        
        if row:
            db.execute_query('DELETE FROM C_LIKE WHERE u_id = ? AND c_id = ?', (u_id, c_id))
        return True
    
    except Exception as e:
        print(f"Error deleting like: {e}")
        db.roll()
        return False

def plyylike_status(pidlist, u_id):
    plikestatus = []
    for pid in pidlist:
        likes = db.get_query('SELECT * FROM P_LIKE WHERE p_id = ? and u_id = ?', (pid, u_id),mul=False)
        plikestatus.append(bool(likes))

    return dict(zip(pidlist, plikestatus))

def plyy_like(p_id, u_id):
    try:
        row = db.get_query('SELECT * FROM P_LIKE WHERE u_id = ? AND p_id = ?', (u_id, p_id),mul=False)
        if not row:
            db.execute_query('INSERT INTO P_LIKE (u_id, p_id) VALUES (?, ?)', (u_id, p_id))

        return True
    
    except Exception as e:
        print(f"Error inserting like: {e}")
        db.roll()
        return False

def plyy_unlike(p_id, u_id):
    try:
        row = db.get_query('SELECT * FROM P_LIKE WHERE u_id = ? AND p_id = ?', (u_id, p_id),mul=False)
        if row:
            db.execute_query('DELETE FROM P_LIKE WHERE u_id = ? AND p_id = ?', (u_id, p_id))
        return True
    
    except Exception as e:
        print(f"Error deleting like: {e}")
        db.roll()
        return False
