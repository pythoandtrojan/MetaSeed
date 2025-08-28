import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self, db_path):
        # Garante que o diretório existe
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            
        self.db_path = db_path
        self.init_db()
        
    def init_db(self):
        try:
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
            print(f"Database initialized successfully at: {self.db_path}")
            
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            # Tenta criar em local alternativo se falhar
            if "unable to open database file" in str(e):
                alt_path = "metaseed.db"
                print(f"Trying alternative path: {alt_path}")
                self.db_path = alt_path
                self.init_db()
        
    def get_connection(self):
        """Método auxiliar para obter conexão com tratamento de erro"""
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None
            
    def add_session(self, session_id, target_ip, target_os, username):
        conn = self.get_connection()
        if conn is None:
            return False
            
        try:
            c = conn.cursor()
            now = datetime.now().isoformat()
            c.execute("INSERT INTO sessions (session_id, target_ip, target_os, username, created_at, last_seen) VALUES (?, ?, ?, ?, ?, ?)",
                      (session_id, target_ip, target_os, username, now, now))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding session: {e}")
            return False
        finally:
            conn.close()
        
    def update_session(self, session_id):
        conn = self.get_connection()
        if conn is None:
            return False
            
        try:
            c = conn.cursor()
            now = datetime.now().isoformat()
            c.execute("UPDATE sessions SET last_seen = ? WHERE session_id = ?", (now, session_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating session: {e}")
            return False
        finally:
            conn.close()
        
    def get_sessions(self):
        conn = self.get_connection()
        if conn is None:
            return []
            
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM sessions ORDER BY last_seen DESC")
            return c.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting sessions: {e}")
            return []
        finally:
            conn.close()
        
    def get_session(self, session_id):
        conn = self.get_connection()
        if conn is None:
            return None
            
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
            return c.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting session: {e}")
            return None
        finally:
            conn.close()
        
    def delete_session(self, session_id):
        conn = self.get_connection()
        if conn is None:
            return False
            
        try:
            c = conn.cursor()
            c.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting session: {e}")
            return False
        finally:
            conn.close()
