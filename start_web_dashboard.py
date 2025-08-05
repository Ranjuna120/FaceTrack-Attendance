#!/usr/bin/env python3
"""
Start Web Dashboard and automatically open browser
"""
import subprocess
import sys
import time
import webbrowser
import threading
from web_dashboard import app

def open_browser():
    """Open browser after server starts"""
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🌐 Starting FaceTrack Web Dashboard...")
    print("📍 URL: http://localhost:5000")
    print("🚀 Opening browser automatically...")
    
    # Start browser in separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
