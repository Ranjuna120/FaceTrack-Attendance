#!/usr/bin/env python3
"""
REST API for mobile app integration
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import hashlib
from datetime import datetime, timedelta
from database_manager import DatabaseManager
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Initialize database
db = DatabaseManager()

def generate_token(user_id):
    """Generate JWT token for authentication"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0'
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Simple login endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Simple authentication (replace with proper user management)
    if username == 'admin' and password == 'admin123':
        token = generate_token(1)
        return jsonify({
            'success': True,
            'token': token,
            'user': {'id': 1, 'username': 'admin', 'role': 'admin'}
        })
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/attendance/mark', methods=['POST'])
def mark_attendance_api():
    """Mark attendance via API"""
    data = request.get_json()
    name = data.get('name')
    location = data.get('location', 'Mobile App')
    
    if not name:
        return jsonify({'success': False, 'message': 'Name is required'}), 400
    
    success, message = db.mark_attendance(name, 'mobile')
    
    return jsonify({
        'success': success,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'location': location
    })

@app.route('/api/attendance/today', methods=['GET'])
def get_today_attendance():
    """Get today's attendance"""
    try:
        df = db.get_attendance_report(days=1)
        attendance_list = df.to_dict('records') if not df.empty else []
        
        return jsonify({
            'success': True,
            'count': len(attendance_list),
            'attendance': attendance_list,
            'date': datetime.now().date().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/attendance/range', methods=['GET'])
def get_attendance_range():
    """Get attendance for date range"""
    days = request.args.get('days', 7, type=int)
    
    try:
        df = db.get_attendance_report(days=days)
        attendance_list = df.to_dict('records') if not df.empty else []
        
        return jsonify({
            'success': True,
            'count': len(attendance_list),
            'attendance': attendance_list,
            'days': days
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, email, department, role FROM users WHERE is_active = 1')
        users = []
        for row in cursor.fetchall():
            users.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'department': row[3],
                'role': row[4]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'users': users,
            'count': len(users)
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create new user"""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    department = data.get('department')
    role = data.get('role')
    
    if not name:
        return jsonify({'success': False, 'message': 'Name is required'}), 400
    
    success, message = db.add_user(name, email, department, role)
    
    return jsonify({
        'success': success,
        'message': message
    }), 201 if success else 400

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get attendance statistics"""
    try:
        # Today's stats
        today_df = db.get_attendance_report(days=1)
        today_count = len(today_df) if not today_df.empty else 0
        
        # Weekly stats
        weekly_df = db.get_attendance_report(days=7)
        weekly_count = len(weekly_df) if not weekly_df.empty else 0
        
        # Monthly stats
        monthly_df = db.get_attendance_report(days=30)
        monthly_count = len(monthly_df) if not monthly_df.empty else 0
        
        return jsonify({
            'success': True,
            'stats': {
                'today': today_count,
                'weekly': weekly_count,
                'monthly': monthly_count,
                'last_updated': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/attendance/export', methods=['GET'])
def export_attendance():
    """Export attendance data"""
    try:
        filename = db.export_to_excel()
        return jsonify({
            'success': True,
            'message': 'Data exported successfully',
            'filename': filename
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("API Server starting at http://localhost:5001")
    print("Available endpoints:")
    print("- GET  /api/health")
    print("- POST /api/auth/login")
    print("- POST /api/attendance/mark")
    print("- GET  /api/attendance/today")
    print("- GET  /api/attendance/range?days=7")
    print("- GET  /api/users")
    print("- POST /api/users")
    print("- GET  /api/stats")
    print("- GET  /api/attendance/export")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
