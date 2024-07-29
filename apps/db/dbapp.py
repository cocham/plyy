import csv
import sqlite3
from database import create_table
import os
from datetime import datetime

db = 'plyy.db'

#DB함수 연결 
def connect_db():
    database_path = os.path.join(os.path.dirname(__file__), 'plyy.db')
    conn = sqlite3.connect(database_path)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur


def insert_track(csv_file):
    conn,cur = connect_db()
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            cur.execute( '''
                            INSERT OR IGNORE INTO TRACK (id, title, artist, album, img, rtime)
                            VALUES (?, ?, ?, ?, ?, ?)
                            ''', (row['id'], row['title'], row['artist'], row['album'], row['img'], row['rtime']))

    conn.commit()
    conn.close()
    
def insert_curator(csv_file):
    conn,cur = connect_db()
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            cur.execute( '''
                            INSERT OR IGNORE INTO CURATOR (name,img,intro)
                            VALUES (?, ?, ?)
                            ''', (row['name'], row['img'], row['intro']))

    conn.commit()
    conn.close()

def insert_genre(csv_file):
    conn,cur = connect_db()
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            cur.execute( '''
                            INSERT OR IGNORE INTO GENRE (name)
                            VALUES (?)
                            ''', (row['name'],))

    conn.commit()
    conn.close()


def insert_plyy(csv_file):
    conn,cur = connect_db()
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            cur.execute( '''
                            INSERT OR IGNORE INTO PLYY (title, img, cmt, c_id, g_id)
                            VALUES (?, ?, ?, ?, ?)
                            ''', (row['title'], row['img'], row['cmt'], int(row['c_id']), int(row['g_id'])))

    conn.commit()
    conn.close()

def insert_song(csv_file):
    conn,cur = connect_db()
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            cur.execute( '''
                            INSERT OR IGNORE INTO PLYY (cmt,vid,p_id)
                            VALUES (?, ?, ?)
                            ''', (row['cmt'], row['vid'],row['p_id']))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    # insert_track('track.csv')
    # insert_curator('./csv/curator.csv')
    # insert_genre('./csv/genre.csv')
    # insert_plyy('./csv/plyy.csv')