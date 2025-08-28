import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()
        
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Tabela de sessões
        c.execute('''CREATE TABLE IF NOT EXISTS sessions
                     (id INTEGER PRIMARY KEY, 
                      session_id TEXT, 
                      target_ip TEXT, 
                      target_os TEXT,
                      username TEXT,
                      created_at TEXT,
                      last_seen TEXT)''')
        
        # Tabela de exploits
        c.execute('''CREATE TABLE IF NOT EXISTS exploits
                     (id INTEGER PRIMARY KEY,
                      name TEXT,
                      description TEXT,
                      platform TEXT,
                      author TEXT,
                      added_date TEXT)''')
        
        # Tabela de módulos
        c.execute('''CREATE TABLE IF NOT EXISTS modules
                     (id INTEGER PRIMARY KEY,
                      name TEXT,
                      type TEXT,
                      description TEXT,
                      options TEXT)''')
        
        conn.commit()
        conn.close()
        
    def add_session(self, session_id, target_ip, target_os, username):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        now = datetime.now().isoformat()
        c.execute("INSERT INTO sessions (session_id, target_ip, target_os, username, created_at, last_seen) VALUES (?, ?, ?, ?, ?, ?)",
                  (session_id, target_ip, target_os, username, now, now))
        
        conn.commit()
        conn.close()
        
    def update_session(self, session_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        now = datetime.now().isoformat()
        c.execute("UPDATE sessions SET last_seen = ? WHERE session_id = ?", (now, session_id))
        
        conn.commit()
        conn.close()
        
    def get_sessions(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT * FROM sessions ORDER BY last_seen DESC")
        sessions = c.fetchall()
        
        conn.close()
        return sessions
        
    def get_session(self, session_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        session = c.fetchone()
        
        conn.close()
        return session
        
    def delete_session(self, session_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        
        conn.commit()
        conn.close()
