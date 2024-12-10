import sqlite3
from datetime import datetime

class DatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect('attendance.db')
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                role TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                check_in TIMESTAMP,
                check_out TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.conn.commit()
    
    def add_user(self, name, role="student"):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (name, role) VALUES (?, ?)", (name, role))
        self.conn.commit()
        return cursor.lastrowid
    
    def mark_attendance(self, user_id):
        cursor = self.conn.cursor()
        now = datetime.now()
        
        # Check if user already has attendance for today
        cursor.execute("""
            SELECT id, check_in, check_out 
            FROM attendance 
            WHERE user_id = ? 
            AND date(check_in) = date(?)
        """, (user_id, now))
        
        record = cursor.fetchone()
        
        if record is None:
            # Create new attendance record
            cursor.execute("""
                INSERT INTO attendance (user_id, check_in)
                VALUES (?, ?)
            """, (user_id, now))
        elif record[2] is None:
            # Update check_out time
            cursor.execute("""
                UPDATE attendance 
                SET check_out = ? 
                WHERE id = ?
            """, (now, record[0]))
            
        self.conn.commit()
    
    def get_attendance_report(self, date=None):
        cursor = self.conn.cursor()
        if date is None:
            date = datetime.now().date()
            
        cursor.execute("""
            SELECT users.name, attendance.check_in, attendance.check_out
            FROM attendance
            JOIN users ON users.id = attendance.user_id
            WHERE date(attendance.check_in) = date(?)
        """, (date,))
        
        return cursor.fetchall() 