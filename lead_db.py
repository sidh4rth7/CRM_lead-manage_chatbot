import sqlite3

conn = sqlite3.connect('lead_db.db')
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS lead
          (
            [id] INTEGER PRIMARY KEY, 
            [name] TEXT, 
            [email] TEXT, 
            [phone_num] TEXT,
            [status] TEXT
          )
          ''')

conn.commit()