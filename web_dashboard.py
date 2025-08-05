#!/usr/bin/env python3
"""
Flask Web Dashboard for Face Recognition Attendance System
"""
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
import os
import json
from datetime import datetime, timedelta
import pandas as pd
from database_manager import DatabaseManager

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Initialize database
db = DatabaseManager()

@app.route('/')
def dashboard():
    """Main dashboard"""
    # Get today's stats
    today = datetime.now().date()
    
    # Get attendance data
    df = db.get_attendance_report(days=1)
    today_count = len(df) if not df.empty else 0
    
    # Get weekly stats
    weekly_df = db.get_attendance_report(days=7)
    weekly_count = len(weekly_df) if not weekly_df.empty else 0
    
    stats = {
        'today_attendance': today_count,
        'weekly_attendance': weekly_count,
        'total_users': len(weekly_df) if not weekly_df.empty else 0,
        'last_update': datetime.now().strftime('%H:%M:%S')
    }
    
    return render_template('dashboard.html', stats=stats)

@app.route('/api/stats')
def api_stats():
    """API endpoint for real-time stats"""
    df = db.get_attendance_report(days=1)
    today_count = len(df) if not df.empty else 0
    
    return jsonify({
        'today_attendance': today_count,
        'last_update': datetime.now().strftime('%H:%M:%S'),
        'recent_attendance': df.to_dict('records') if not df.empty else []
    })

@app.route('/users')
def users():
    """Users management page"""
    return render_template('users.html')

@app.route('/reports')
def reports():
    """Reports page"""
    return render_template('reports.html')

@app.route('/api/attendance/mark', methods=['POST'])
def mark_attendance():
    """API to mark attendance manually"""
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'success': False, 'message': 'Name is required'})
    
    success, message = db.mark_attendance(name, 'manual')
    return jsonify({'success': success, 'message': message})

if __name__ == '__main__':
    # Create templates directory and basic templates
    os.makedirs('templates', exist_ok=True)
    
    # Create basic dashboard template
    dashboard_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Attendance Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="#">FaceTrack Attendance</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Dashboard</a>
                <a class="nav-link" href="/users">Users</a>
                <a class="nav-link" href="/reports">Reports</a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <div class="row">
            <div class="col-md-3">
                <div class="card text-white bg-success">
                    <div class="card-body">
                        <h5 class="card-title">Today's Attendance</h5>
                        <h2 id="today-count">{{ stats.today_attendance }}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-info">
                    <div class="card-body">
                        <h5 class="card-title">This Week</h5>
                        <h2>{{ stats.weekly_attendance }}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-warning">
                    <div class="card-body">
                        <h5 class="card-title">Total Users</h5>
                        <h2>{{ stats.total_users }}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-secondary">
                    <div class="card-body">
                        <h5 class="card-title">Last Update</h5>
                        <p id="last-update">{{ stats.last_update }}</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>Manual Attendance</h5>
                    </div>
                    <div class="card-body">
                        <div class="input-group">
                            <input type="text" id="manual-name" class="form-control" placeholder="Enter name">
                            <button class="btn btn-primary" onclick="markAttendance()">Mark Attendance</button>
                        </div>
                        <div id="message" class="mt-2"></div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>Recent Attendance</h5>
                    </div>
                    <div class="card-body">
                        <div id="recent-list">Loading...</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function markAttendance() {
            const name = document.getElementById('manual-name').value;
            if (!name) return;
            
            fetch('/api/attendance/mark', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: name})
            })
            .then(response => response.json())
            .then(data => {
                const messageDiv = document.getElementById('message');
                messageDiv.className = data.success ? 'alert alert-success' : 'alert alert-danger';
                messageDiv.textContent = data.message;
                if (data.success) {
                    document.getElementById('manual-name').value = '';
                    updateStats();
                }
            });
        }
        
        function updateStats() {
            fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                document.getElementById('today-count').textContent = data.today_attendance;
                document.getElementById('last-update').textContent = data.last_update;
                
                const recentList = document.getElementById('recent-list');
                if (data.recent_attendance.length > 0) {
                    recentList.innerHTML = data.recent_attendance.map(item => 
                        `<div class="d-flex justify-content-between">
                            <span>${item.name}</span>
                            <small>${item.last_attendance}</small>
                        </div>`
                    ).join('');
                } else {
                    recentList.innerHTML = '<p class="text-muted">No attendance today</p>';
                }
            });
        }
        
        // Update stats every 30 seconds
        setInterval(updateStats, 30000);
        updateStats();
    </script>
</body>
</html>
    '''
    
    with open('templates/dashboard.html', 'w') as f:
        f.write(dashboard_html)
    
    print("Web dashboard starting at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
