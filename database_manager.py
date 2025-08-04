#!/usr/bin/env python3
"""
Database integration for Face Recognition Attendance System
"""
import sqlite3
import pandas as pd
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path="data/attendance.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                email TEXT,
                department TEXT,
                role TEXT,
                registered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Create attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                type TEXT DEFAULT 'auto',  -- 'auto' or 'manual'
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create sessions table for tracking active sessions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                check_in TIMESTAMP,
                check_out TIMESTAMP,
                duration INTEGER,  -- in minutes
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, name, email=None, department=None, role=None):
        """Add a new user to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (name, email, department, role)
                VALUES (?, ?, ?, ?)
            ''', (name, email, department, role))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return True, f"User {name} added with ID {user_id}"
        except sqlite3.IntegrityError:
            conn.close()
            return False, f"User {name} already exists"
    
    def mark_attendance(self, name, attendance_type='auto'):
        """Mark attendance for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get user ID
        cursor.execute('SELECT id FROM users WHERE name = ? AND is_active = 1', (name,))
        user = cursor.fetchone()
        
        if not user:
            # Auto-create user if doesn't exist
            cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
            user_id = cursor.lastrowid
        else:
            user_id = user[0]
        
        # Check if already marked today
        today = datetime.now().date()
        cursor.execute('''
            SELECT id FROM attendance 
            WHERE user_id = ? AND DATE(timestamp) = ?
        ''', (user_id, today))
        
        if cursor.fetchone():
            conn.close()
            return False, f"Attendance already marked for {name} today"
        
        # Mark attendance
        cursor.execute('''
            INSERT INTO attendance (user_id, type)
            VALUES (?, ?)
        ''', (user_id, attendance_type))
        
        conn.commit()
        conn.close()
        return True, f"Attendance marked for {name}"
    
    def get_attendance_report(self, days=30):
        """Get attendance report for last N days"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT u.name, u.department, u.role, 
                   COUNT(a.id) as attendance_count,
                   MAX(a.timestamp) as last_attendance
            FROM users u
            LEFT JOIN attendance a ON u.id = a.user_id
            WHERE a.timestamp >= datetime('now', '-{} days')
            GROUP BY u.id, u.name
            ORDER BY attendance_count DESC
        '''.format(days)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def export_to_excel(self, filename=None):
        """Export all data to Excel with multiple sheets"""
        filename = filename or f"data/attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        conn = sqlite3.connect(self.db_path)
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Users sheet
            users_df = pd.read_sql_query('SELECT * FROM users', conn)
            users_df.to_excel(writer, sheet_name='Users', index=False)
            
            # Attendance sheet
            attendance_query = '''
                SELECT u.name, u.department, a.timestamp, a.type
                FROM attendance a
                JOIN users u ON a.user_id = u.id
                ORDER BY a.timestamp DESC
            '''
            attendance_df = pd.read_sql_query(attendance_query, conn)
            attendance_df.to_excel(writer, sheet_name='Attendance', index=False)
            
            # Summary sheet
            summary_df = self.get_attendance_report()
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        conn.close()
        return f"Data exported to {filename}"
