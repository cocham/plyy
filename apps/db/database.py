import sqlite3

# SQLite 데이터베이스 연결 설정
conn = sqlite3.connect('plyy.db')
cursor = conn.cursor()


def create_table():
    # TRACK 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TRACK (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            album TEXT NOT NULL,
            img TEXT NOT NULL,
            rtime INTEGER NOT NULL
        )
    ''')

    # PLYY 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS 'PLYY' (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'title' TEXT NOT NULL,
        'img' TEXT NOT NULL,
        'gen_date' DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        'up_date' DATETIME,
        'cmt' TEXT NOT NULL,
        'c_id' TEXT NOT NULL,
        'g_id' TEXT NOT NULL,
        FOREIGN KEY ('c_id') REFERENCES CURATOR("id"),
        FOREIGN KEY ('g_id') REFERENCES GENRE("id")
        )     
    ''')

    #curator 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'CURATOR' (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'name' TEXT NOT NULL UNIQUE,
        'img' TEXT NOT NULL,
        'intro' TEXT NOT NULL
        )
    ''')

    #song 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'SONG' (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'cmt' TEXT,
        'vid' TEXT NOT NULL,
        'index' INTEGER NOT NULL,
        'p_id' INTEGER NOT NULL,
        'tk_id' TEXT NOT NULL,
        FOREIGN KEY ('p_id') REFERENCES PLYY("id") ON DELETE CASCADE,
        FOREIGN KEY ('tk_id') REFERENCES TRACK("id") ON DELETE CASCADE
        )   
    ''')

    #USER 테이블 생성
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS 'USER' (
            'id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'email' TEXT NOT NULL UNIQUE,
            'pw' TEXT NOT NULL,
            'nickname' TEXT,
            'img' TEXT
        )
    ''')

    #P_LIKE 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'P_LIKE' (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'u_id' INTEGER,
        'p_id' INTEGER,
        FOREIGN KEY ('u_id') REFERENCES USER("id") ON DELETE CASCADE,
        FOREIGN KEY ('p_id') REFERENCES PLYY("id") ON DELETE CASCADE
        )
    ''')    

    #C_LIKE 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'C_LIKE' (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'u_id' INTEGER,
        'c_id' INTEGER,
        FOREIGN KEY ('u_id') REFERENCES USER("id") ON DELETE CASCADE,
        FOREIGN KEY ('c_id') REFERENCES CURATOR("id") ON DELETE CASCADE
        )
    ''')    

    #TAG 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'TAG' (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'name' TEXT NOT NULL
        )
    ''')
    
    #P_TAG 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'P_TAG' (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT,
        't_id' INTEGER,
        'p_id' INTEGER,
        FOREIGN KEY ('t_id') REFERENCES TAG("id") ON DELETE CASCADE,
        FOREIGN KEY ('p_id') REFERENCES PLYY("id") ON DELETE CASCADE
        )
    ''')

    #C_TAG 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'C_TAG' (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT,
        't_id' INTEGER,
        'c_id' INTEGER,
        FOREIGN KEY ('t_id') REFERENCES TAG("id") ON DELETE CASCADE,
        FOREIGN KEY ('c_id') REFERENCES CURATOR("id") ON DELETE CASCADE
        )
    ''')

    #GENRE 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'GENRE' (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'name' TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
