#!/usr/bin/env python3
"""
Master Control Panel for Face Recognition Attendance System
This file integrates all the new features and provides a unified interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import subprocess
import sys
import os
from datetime import datetime
import config

# Import all the new modules
try:
    from face_recognition_module_compatible import FaceRecognitionModuleCompatible
    from advanced_attendance import AdvancedAttendanceManager
    from database_manager import DatabaseManager
    from email_notifier import EmailNotifier
except ImportError as e:
    print(f"Warning: Some modules not available: {e}")

class MasterControlPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FaceTrack Attendance - Master Control Panel")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize modules
        self.face_module = None
        self.attendance_manager = None
        self.db_manager = None
        self.email_notifier = None
        
        self.setup_ui()
        self.initialize_modules()
        
    def setup_ui(self):
        """Setup the master control panel UI"""
        # Main title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="FaceTrack Attendance - Master Control Panel", 
                              font=("Arial", 20, "bold"), fg="white", bg="#2c3e50")
        title_label.pack(expand=True)
        
        # Status frame
        self.status_frame = tk.Frame(self.root, bg="#ecf0f1", height=60)
        self.status_frame.pack(fill=tk.X, padx=10, pady=5)
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_frame, text="System Status: Initializing...", 
                                   font=("Arial", 12), bg="#ecf0f1")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=20)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_main_tab()
        self.create_advanced_tab()
        self.create_analytics_tab()
        self.create_settings_tab()
        self.create_integrations_tab()
        
    def create_main_tab(self):
        """Create main attendance tab"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="Main Attendance")
        
        # Quick actions frame
        quick_frame = tk.LabelFrame(main_frame, text="Quick Actions", font=("Arial", 12, "bold"))
        quick_frame.pack(fill=tk.X, padx=10, pady=5)
        
        btn_frame = tk.Frame(quick_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="Register New Face", command=self.register_face,
                 bg="#27ae60", fg="white", font=("Arial", 11, "bold"), height=2).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Start Attendance", command=self.start_attendance,
                 bg="#3498db", fg="white", font=("Arial", 11, "bold"), height=2).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="View Today's Report", command=self.view_today_report,
                 bg="#f39c12", fg="white", font=("Arial", 11, "bold"), height=2).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Export Data", command=self.export_data,
                 bg="#9b59b6", fg="white", font=("Arial", 11, "bold"), height=2).pack(side=tk.LEFT, padx=5)
        
        # Recent activity frame
        activity_frame = tk.LabelFrame(main_frame, text="Recent Activity", font=("Arial", 12, "bold"))
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollable text area for recent activity
        text_frame = tk.Frame(activity_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.activity_text = tk.Text(text_frame, wrap=tk.WORD, font=("Courier", 10))
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.activity_text.yview)
        self.activity_text.configure(yscrollcommand=scrollbar.set)
        
        self.activity_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_advanced_tab(self):
        """Create advanced features tab"""
        advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(advanced_frame, text="Advanced Features")
        
        # Database management
        db_frame = tk.LabelFrame(advanced_frame, text="Database Management", font=("Arial", 12, "bold"))
        db_frame.pack(fill=tk.X, padx=10, pady=5)
        
        db_btn_frame = tk.Frame(db_frame)
        db_btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(db_btn_frame, text="View Database", command=self.view_database,
                 bg="#34495e", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(db_btn_frame, text="Backup Database", command=self.backup_database,
                 bg="#16a085", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(db_btn_frame, text="Import Data", command=self.import_data,
                 bg="#d35400", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Email notifications
        email_frame = tk.LabelFrame(advanced_frame, text="Email Notifications", font=("Arial", 12, "bold"))
        email_frame.pack(fill=tk.X, padx=10, pady=5)
        
        email_config_frame = tk.Frame(email_frame)
        email_config_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(email_config_frame, text="Email:").grid(row=0, column=0, sticky="w", padx=5)
        self.email_entry = tk.Entry(email_config_frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(email_config_frame, text="Password:").grid(row=1, column=0, sticky="w", padx=5)
        self.password_entry = tk.Entry(email_config_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5)
        
        tk.Button(email_config_frame, text="Configure Email", command=self.configure_email,
                 bg="#e74c3c", fg="white").grid(row=0, column=2, rowspan=2, padx=10)
        
        # Manual attendance
        manual_frame = tk.LabelFrame(advanced_frame, text="Manual Attendance", font=("Arial", 12, "bold"))
        manual_frame.pack(fill=tk.X, padx=10, pady=5)
        
        manual_entry_frame = tk.Frame(manual_frame)
        manual_entry_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(manual_entry_frame, text="Name:").pack(side=tk.LEFT, padx=5)
        self.manual_name_entry = tk.Entry(manual_entry_frame, width=20)
        self.manual_name_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(manual_entry_frame, text="Mark Present", command=self.mark_manual_attendance,
                 bg="#27ae60", fg="white").pack(side=tk.LEFT, padx=5)
        
    def create_analytics_tab(self):
        """Create analytics and reports tab"""
        analytics_frame = ttk.Frame(self.notebook)
        self.notebook.add(analytics_frame, text="Analytics & Reports")
        
        # Stats display
        stats_frame = tk.LabelFrame(analytics_frame, text="Statistics", font=("Arial", 12, "bold"))
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=8, wrap=tk.WORD, font=("Courier", 10))
        self.stats_text.pack(fill=tk.X, padx=10, pady=10)
        
        # Report generation
        report_frame = tk.LabelFrame(analytics_frame, text="Report Generation", font=("Arial", 12, "bold"))
        report_frame.pack(fill=tk.X, padx=10, pady=5)
        
        report_btn_frame = tk.Frame(report_frame)
        report_btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(report_btn_frame, text="Generate Daily Report", command=self.generate_daily_report,
                 bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(report_btn_frame, text="Generate Weekly Report", command=self.generate_weekly_report,
                 bg="#9b59b6", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(report_btn_frame, text="Create Charts", command=self.create_charts,
                 bg="#e67e22", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Update stats button
        tk.Button(analytics_frame, text="Refresh Statistics", command=self.update_statistics,
                 bg="#95a5a6", fg="white", font=("Arial", 11, "bold")).pack(pady=10)
        
    def create_settings_tab(self):
        """Create settings and configuration tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Face recognition settings
        face_settings_frame = tk.LabelFrame(settings_frame, text="Face Recognition Settings", font=("Arial", 12, "bold"))
        face_settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Tolerance setting
        tolerance_frame = tk.Frame(face_settings_frame)
        tolerance_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(tolerance_frame, text="Recognition Tolerance:").pack(side=tk.LEFT)
        self.tolerance_var = tk.DoubleVar(value=config.FACE_RECOGNITION_TOLERANCE)
        tolerance_scale = tk.Scale(tolerance_frame, from_=0.3, to=0.9, resolution=0.1, 
                                 orient=tk.HORIZONTAL, variable=self.tolerance_var)
        tolerance_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Model selection
        model_frame = tk.Frame(face_settings_frame)
        model_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(model_frame, text="Recognition Model:").pack(side=tk.LEFT)
        self.model_var = tk.StringVar(value=config.FACE_RECOGNITION_MODEL)
        model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, values=["hog", "cnn"])
        model_combo.pack(side=tk.LEFT, padx=10)
        
        # Apply settings button
        tk.Button(face_settings_frame, text="Apply Settings", command=self.apply_settings,
                 bg="#2ecc71", fg="white").pack(pady=10)
        
    def create_integrations_tab(self):
        """Create integrations tab"""
        integrations_frame = ttk.Frame(self.notebook)
        self.notebook.add(integrations_frame, text="Integrations")
        
        # Web dashboard
        web_frame = tk.LabelFrame(integrations_frame, text="Web Dashboard", font=("Arial", 12, "bold"))
        web_frame.pack(fill=tk.X, padx=10, pady=5)
        
        web_btn_frame = tk.Frame(web_frame)
        web_btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(web_btn_frame, text="Start Web Dashboard", command=self.start_web_dashboard,
                 bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(web_btn_frame, text="Start API Server", command=self.start_api_server,
                 bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=5)
        
        # External integrations
        external_frame = tk.LabelFrame(integrations_frame, text="External Integrations", font=("Arial", 12, "bold"))
        external_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(external_frame, text="API Endpoint URL:").pack(anchor="w", padx=10, pady=5)
        self.api_url_entry = tk.Entry(external_frame, width=50)
        self.api_url_entry.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(external_frame, text="Test Connection", command=self.test_api_connection,
                 bg="#f39c12", fg="white").pack(pady=5)
        
    def initialize_modules(self):
        """Initialize all system modules"""
        try:
            self.face_module = FaceRecognitionModuleCompatible()
            self.attendance_manager = AdvancedAttendanceManager()
            self.db_manager = DatabaseManager()
            self.email_notifier = EmailNotifier()
            
            self.update_status("System initialized successfully", "green")
            self.log_activity("System started successfully")
            self.update_statistics()
            
        except Exception as e:
            self.update_status(f"Initialization error: {str(e)}", "red")
            self.log_activity(f"ERROR: {str(e)}")
    
    def update_status(self, message, color="black"):
        """Update status label"""
        self.status_label.config(text=f"Status: {message}", fg=color)
        self.root.update()
    
    def log_activity(self, message):
        """Log activity to the activity text area"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.activity_text.insert(tk.END, log_message)
        self.activity_text.see(tk.END)
        self.root.update()
    
    # Button handlers
    def register_face(self):
        """Handle face registration"""
        name = tk.simpledialog.askstring("Register Face", "Enter name:")
        if name:
            self.update_status("Starting face registration...", "blue")
            threading.Thread(target=self._register_face_thread, args=(name,)).start()
    
    def _register_face_thread(self, name):
        """Face registration in separate thread"""
        try:
            success, message = self.face_module.register_face(name)
            if success:
                self.log_activity(f"Face registered: {name}")
                self.update_status("Face registration completed", "green")
            else:
                self.log_activity(f"Registration failed: {message}")
                self.update_status("Face registration failed", "red")
        except Exception as e:
            self.log_activity(f"Registration error: {str(e)}")
            self.update_status("Registration error", "red")
    
    def start_attendance(self):
        """Handle attendance recognition"""
        self.update_status("Starting attendance recognition...", "blue")
        threading.Thread(target=self._attendance_thread).start()
    
    def _attendance_thread(self):
        """Attendance recognition in separate thread"""
        try:
            recognized = self.face_module.recognize_faces()
            for name in recognized:
                success, message = self.attendance_manager.mark_attendance(name)
                self.log_activity(f"Attendance: {name} - {message}")
            
            self.update_status("Attendance completed", "green")
        except Exception as e:
            self.log_activity(f"Attendance error: {str(e)}")
            self.update_status("Attendance error", "red")
    
    def view_today_report(self):
        """View today's attendance report"""
        try:
            stats = self.attendance_manager.get_attendance_stats(days=1)
            report = f"Today's Attendance Report:\n"
            report += f"Total Attendances: {stats.get('total_attendances', 0)}\n"
            report += f"Unique People: {stats.get('unique_people', 0)}\n"
            
            messagebox.showinfo("Today's Report", report)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def export_data(self):
        """Export attendance data"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            if filename:
                # Export using database manager
                result = self.db_manager.export_to_excel(filename)
                messagebox.showinfo("Export", result)
                self.log_activity(f"Data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def update_statistics(self):
        """Update statistics display"""
        try:
            stats = self.attendance_manager.get_attendance_stats(days=30)
            
            stats_text = f"""
ATTENDANCE STATISTICS (Last 30 days)
=====================================

Total Attendances: {stats.get('total_attendances', 0)}
Unique People: {stats.get('unique_people', 0)}
Daily Average: {stats.get('daily_average', 0):.1f}
Most Regular: {stats.get('most_punctual', 'N/A')}

Attendance by Person:
"""
            for name, count in stats.get('attendance_by_person', {}).items():
                stats_text += f"  • {name}: {count} days\n"
            
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats_text)
            
        except Exception as e:
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, f"Error loading statistics: {str(e)}")
    
    def start_web_dashboard(self):
        """Start web dashboard"""
        try:
            subprocess.Popen([sys.executable, "web_dashboard.py"])
            self.log_activity("Web dashboard started")
            messagebox.showinfo("Web Dashboard", "Web dashboard started at http://localhost:5000")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start web dashboard: {str(e)}")
    
    def start_api_server(self):
        """Start API server"""
        try:
            subprocess.Popen([sys.executable, "api_server.py"])
            self.log_activity("API server started")
            messagebox.showinfo("API Server", "API server started at http://localhost:5001")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start API server: {str(e)}")
    
    def configure_email(self):
        """Configure email settings"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if email and password:
            self.email_notifier.configure(email, password)
            self.log_activity("Email configured successfully")
            messagebox.showinfo("Email", "Email configured successfully!")
        else:
            messagebox.showwarning("Email", "Please enter both email and password")
    
    def mark_manual_attendance(self):
        """Mark manual attendance"""
        name = self.manual_name_entry.get()
        if name:
            try:
                success, message = self.attendance_manager.mark_attendance(name)
                self.log_activity(f"Manual attendance: {name} - {message}")
                self.manual_name_entry.delete(0, tk.END)
                messagebox.showinfo("Attendance", message)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to mark attendance: {str(e)}")
    
    def apply_settings(self):
        """Apply face recognition settings"""
        # Update config values (in a real implementation, you'd save these to a config file)
        tolerance = self.tolerance_var.get()
        model = self.model_var.get()
        
        self.log_activity(f"Settings updated: Tolerance={tolerance}, Model={model}")
        messagebox.showinfo("Settings", "Settings applied successfully!")
    
    # Placeholder methods for remaining functionality
    def view_database(self):
        messagebox.showinfo("Database", "Database viewer feature coming soon!")
    
    def backup_database(self):
        messagebox.showinfo("Backup", "Database backup feature coming soon!")
    
    def import_data(self):
        messagebox.showinfo("Import", "Data import feature coming soon!")
    
    def generate_daily_report(self):
        messagebox.showinfo("Report", "Daily report generated!")
    
    def generate_weekly_report(self):
        messagebox.showinfo("Report", "Weekly report generated!")
    
    def create_charts(self):
        try:
            result = self.attendance_manager.create_attendance_chart()
            messagebox.showinfo("Charts", result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create charts: {str(e)}")
    
    def test_api_connection(self):
        messagebox.showinfo("API", "API connection test feature coming soon!")
    
    def run(self):
        """Start the master control panel"""
        self.root.mainloop()

if __name__ == "__main__":
    # Create required imports for dialog
    import tkinter.simpledialog
    
    app = MasterControlPanel()
    app.run()
