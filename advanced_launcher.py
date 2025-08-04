#!/usr/bin/env python3
"""
Quick Launcher for Advanced Features
"""
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
import os

class QuickLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FaceTrack - Advanced Features Launcher")
        self.root.geometry("500x400")
        self.root.configure(bg="#2c3e50")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="🎛️ FaceTrack Advanced Features", 
                        font=("Arial", 18, "bold"), fg="white", bg="#2c3e50")
        title.pack(pady=20)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#34495e", relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Buttons
        buttons = [
            ("🎛️ Master Control Panel", self.open_master_control, "#e74c3c"),
            ("🌐 Web Dashboard", self.open_web_dashboard, "#3498db"),
            ("📱 API Server", self.open_api_server, "#2ecc71"),
            ("📊 Analytics Dashboard", self.open_analytics, "#f39c12"),
            ("🗄️ Database Manager", self.open_database, "#9b59b6"),
            ("📧 Email Notifications", self.open_email, "#e67e22"),
            ("💻 Command Line Interface", self.open_cli, "#95a5a6"),
            ("🔧 Test All Features", self.test_features, "#1abc9c")
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(main_frame, text=text, command=command,
                          font=("Arial", 11, "bold"), bg=color, fg="white",
                          height=2, relief=tk.FLAT, cursor="hand2")
            btn.pack(fill=tk.X, padx=15, pady=5)
    
    def run_script(self, script_name):
        """Run a Python script"""
        try:
            subprocess.Popen([sys.executable, script_name])
            messagebox.showinfo("Launched", f"{script_name} started successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start {script_name}: {e}")
    
    def open_master_control(self):
        self.run_script("master_control.py")
    
    def open_web_dashboard(self):
        self.run_script("web_dashboard.py")
        messagebox.showinfo("Web Dashboard", "Access at: http://localhost:5000")
    
    def open_api_server(self):
        self.run_script("api_server.py")
        messagebox.showinfo("API Server", "Access at: http://localhost:5001")
    
    def open_analytics(self):
        self.run_script("simple_advanced_attendance.py")
    
    def open_database(self):
        try:
            from database_manager import DatabaseManager
            db = DatabaseManager()
            messagebox.showinfo("Database", f"Database location: {db.db_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
    
    def open_email(self):
        try:
            from email_notifier import EmailNotifier
            messagebox.showinfo("Email", "Email notifier module loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Email module error: {e}")
    
    def open_cli(self):
        self.run_script("cli_test.py")
    
    def test_features(self):
        self.run_script("test_all_features.py")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    launcher = QuickLauncher()
    launcher.run()
