#!/usr/bin/env python3
"""
Email Notifications Configuration and Testing Interface
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from email_notifier import EmailNotifier
from simple_advanced_attendance import SimpleAdvancedAttendanceManager
import pandas as pd
from datetime import datetime
import threading

class EmailNotificationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📧 Email Notifications - FaceTrack Attendance")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        
        self.email_notifier = EmailNotifier()
        self.attendance_manager = SimpleAdvancedAttendanceManager()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📧 Email Notifications Configuration", 
                              font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
        title_label.pack(expand=True)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_config_tab()
        self.create_test_tab()
        self.create_reports_tab()
        self.create_help_tab()
    
    def create_config_tab(self):
        """Email Configuration Tab"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuration")
        
        # Email settings
        settings_frame = tk.LabelFrame(config_frame, text="Email Settings", font=("Arial", 12, "bold"))
        settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # SMTP Server
        tk.Label(settings_frame, text="SMTP Server:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.smtp_entry = tk.Entry(settings_frame, width=30)
        self.smtp_entry.insert(0, "smtp.gmail.com")
        self.smtp_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # SMTP Port
        tk.Label(settings_frame, text="SMTP Port:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.port_entry = tk.Entry(settings_frame, width=10)
        self.port_entry.insert(0, "587")
        self.port_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Sender Email
        tk.Label(settings_frame, text="Sender Email:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.sender_email_entry = tk.Entry(settings_frame, width=30)
        self.sender_email_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Sender Password
        tk.Label(settings_frame, text="App Password:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.sender_password_entry = tk.Entry(settings_frame, width=30, show="*")
        self.sender_password_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Recipient Email
        tk.Label(settings_frame, text="Recipient Email:", font=("Arial", 10)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.recipient_email_entry = tk.Entry(settings_frame, width=30)
        self.recipient_email_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Configure button
        configure_btn = tk.Button(settings_frame, text="💾 Save Configuration", 
                                command=self.configure_email, bg="#27ae60", fg="white",
                                font=("Arial", 10, "bold"))
        configure_btn.grid(row=5, column=0, columnspan=2, pady=15)
        
        # Status
        self.config_status = tk.Label(settings_frame, text="Status: Not configured", 
                                    font=("Arial", 10), fg="red")
        self.config_status.grid(row=6, column=0, columnspan=2, pady=5)
    
    def create_test_tab(self):
        """Email Testing Tab"""
        test_frame = ttk.Frame(self.notebook)
        self.notebook.add(test_frame, text="🧪 Test Emails")
        
        # Test buttons
        test_buttons_frame = tk.Frame(test_frame)
        test_buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(test_buttons_frame, text="📨 Send Test Email", 
                 command=self.send_test_email, bg="#3498db", fg="white",
                 font=("Arial", 11, "bold"), height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(test_buttons_frame, text="📊 Send Daily Report", 
                 command=self.send_daily_report, bg="#e67e22", fg="white",
                 font=("Arial", 11, "bold"), height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(test_buttons_frame, text="🚨 Send Attendance Alert", 
                 command=self.send_attendance_alert, bg="#e74c3c", fg="white",
                 font=("Arial", 11, "bold"), height=2).pack(side=tk.LEFT, padx=5)
        
        # Test results
        results_frame = tk.LabelFrame(test_frame, text="Test Results", font=("Arial", 12, "bold"))
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.test_results = scrolledtext.ScrolledText(results_frame, height=15, font=("Courier", 10))
        self.test_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_reports_tab(self):
        """Automated Reports Tab"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="📋 Automated Reports")
        
        # Schedule settings
        schedule_frame = tk.LabelFrame(reports_frame, text="Report Schedule", font=("Arial", 12, "bold"))
        schedule_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Daily reports
        self.daily_enabled = tk.BooleanVar()
        daily_check = tk.Checkbutton(schedule_frame, text="Enable Daily Reports", 
                                   variable=self.daily_enabled, font=("Arial", 10))
        daily_check.pack(anchor="w", padx=10, pady=5)
        
        # Weekly reports
        self.weekly_enabled = tk.BooleanVar()
        weekly_check = tk.Checkbutton(schedule_frame, text="Enable Weekly Reports", 
                                    variable=self.weekly_enabled, font=("Arial", 10))
        weekly_check.pack(anchor="w", padx=10, pady=5)
        
        # Instant alerts
        self.alerts_enabled = tk.BooleanVar()
        alerts_check = tk.Checkbutton(schedule_frame, text="Enable Instant Attendance Alerts", 
                                    variable=self.alerts_enabled, font=("Arial", 10))
        alerts_check.pack(anchor="w", padx=10, pady=5)
        
        # Apply schedule
        schedule_btn = tk.Button(schedule_frame, text="✅ Apply Schedule", 
                               command=self.apply_schedule, bg="#9b59b6", fg="white",
                               font=("Arial", 10, "bold"))
        schedule_btn.pack(pady=10)
        
        # Recent reports
        recent_frame = tk.LabelFrame(reports_frame, text="Recent Reports", font=("Arial", 12, "bold"))
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.recent_reports = scrolledtext.ScrolledText(recent_frame, height=10, font=("Courier", 10))
        self.recent_reports.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load recent reports
        self.load_recent_reports()
    
    def create_help_tab(self):
        """Help Tab"""
        help_frame = ttk.Frame(self.notebook)
        self.notebook.add(help_frame, text="❓ Help")
        
        help_text = """
📧 EMAIL NOTIFICATIONS HELP
=========================

🔧 CONFIGURATION:
1. Enter your email settings in the Configuration tab
2. For Gmail, use "smtp.gmail.com" and port 587
3. Use an App Password (not your regular password)
4. Save the configuration

🧪 TESTING:
1. Send a test email to verify settings work
2. Test daily reports to see the format
3. Test attendance alerts for individual notifications

📋 AUTOMATED REPORTS:
1. Enable daily/weekly reports as needed
2. Configure instant alerts for real-time notifications
3. View recent reports in the Recent Reports section

🔐 GMAIL SETUP:
1. Enable 2-Factor Authentication
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Use this password (not your Gmail password)

📨 EMAIL TYPES:
• Test Email: Simple verification email
• Daily Report: Attendance summary for the day
• Attendance Alert: Instant notification when someone marks attendance
• Weekly Summary: Comprehensive weekly report

⚠️ TROUBLESHOOTING:
• "Authentication failed": Check email/password
• "Connection failed": Check SMTP server/port
• "No data": Ensure attendance records exist
        """
        
        help_text_widget = scrolledtext.ScrolledText(help_frame, font=("Courier", 10))
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.config(state=tk.DISABLED)
    
    def configure_email(self):
        """Configure email settings"""
        sender_email = self.sender_email_entry.get()
        sender_password = self.sender_password_entry.get()
        
        if not sender_email or not sender_password:
            messagebox.showwarning("Configuration", "Please enter both email and password!")
            return
        
        try:
            self.email_notifier.configure(sender_email, sender_password)
            self.config_status.config(text="Status: Configured ✅", fg="green")
            messagebox.showinfo("Configuration", "Email configured successfully!")
        except Exception as e:
            self.config_status.config(text=f"Status: Error - {str(e)}", fg="red")
            messagebox.showerror("Configuration Error", f"Failed to configure email: {str(e)}")
    
    def send_test_email(self):
        """Send test email"""
        recipient = self.recipient_email_entry.get()
        if not recipient:
            messagebox.showwarning("Test Email", "Please enter recipient email!")
            return
        
        def send_email():
            try:
                # Create test data
                test_data = pd.DataFrame([
                    {"Name": "Test User", "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                ])
                
                success, message = self.email_notifier.send_daily_report(recipient, test_data)
                
                result = f"[{datetime.now().strftime('%H:%M:%S')}] Test Email: {message}\n"
                self.test_results.insert(tk.END, result)
                self.test_results.see(tk.END)
                
                if success:
                    messagebox.showinfo("Test Email", "Test email sent successfully!")
                else:
                    messagebox.showerror("Test Email", f"Failed to send: {message}")
                    
            except Exception as e:
                error_msg = f"[{datetime.now().strftime('%H:%M:%S')}] Test Email Error: {str(e)}\n"
                self.test_results.insert(tk.END, error_msg)
                self.test_results.see(tk.END)
                messagebox.showerror("Test Email", f"Error: {str(e)}")
        
        # Run in separate thread to prevent GUI freezing
        threading.Thread(target=send_email, daemon=True).start()
    
    def send_daily_report(self):
        """Send daily report"""
        recipient = self.recipient_email_entry.get()
        if not recipient:
            messagebox.showwarning("Daily Report", "Please enter recipient email!")
            return
        
        def send_report():
            try:
                # Get today's attendance data
                stats = self.attendance_manager.get_attendance_stats(days=1)
                
                # Create DataFrame from stats
                attendance_data = []
                for name, count in stats.get('attendance_by_person', {}).items():
                    attendance_data.append({
                        "Name": name,
                        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                
                df = pd.DataFrame(attendance_data)
                
                success, message = self.email_notifier.send_daily_report(recipient, df)
                
                result = f"[{datetime.now().strftime('%H:%M:%S')}] Daily Report: {message}\n"
                self.test_results.insert(tk.END, result)
                self.test_results.see(tk.END)
                
                if success:
                    messagebox.showinfo("Daily Report", "Daily report sent successfully!")
                else:
                    messagebox.showerror("Daily Report", f"Failed to send: {message}")
                    
            except Exception as e:
                error_msg = f"[{datetime.now().strftime('%H:%M:%S')}] Daily Report Error: {str(e)}\n"
                self.test_results.insert(tk.END, error_msg)
                self.test_results.see(tk.END)
                messagebox.showerror("Daily Report", f"Error: {str(e)}")
        
        threading.Thread(target=send_report, daemon=True).start()
    
    def send_attendance_alert(self):
        """Send attendance alert"""
        recipient = self.recipient_email_entry.get()
        if not recipient:
            messagebox.showwarning("Attendance Alert", "Please enter recipient email!")
            return
        
        def send_alert():
            try:
                success, message = self.email_notifier.send_attendance_alert(recipient, "Test User")
                
                result = f"[{datetime.now().strftime('%H:%M:%S')}] Attendance Alert: {message}\n"
                self.test_results.insert(tk.END, result)
                self.test_results.see(tk.END)
                
                if success:
                    messagebox.showinfo("Attendance Alert", "Attendance alert sent successfully!")
                else:
                    messagebox.showerror("Attendance Alert", f"Failed to send: {message}")
                    
            except Exception as e:
                error_msg = f"[{datetime.now().strftime('%H:%M:%S')}] Attendance Alert Error: {str(e)}\n"
                self.test_results.insert(tk.END, error_msg)
                self.test_results.see(tk.END)
                messagebox.showerror("Attendance Alert", f"Error: {str(e)}")
        
        threading.Thread(target=send_alert, daemon=True).start()
    
    def apply_schedule(self):
        """Apply email schedule settings"""
        settings = {
            "daily_reports": self.daily_enabled.get(),
            "weekly_reports": self.weekly_enabled.get(),
            "instant_alerts": self.alerts_enabled.get()
        }
        
        messagebox.showinfo("Schedule", f"Email schedule applied:\n" +
                          f"Daily Reports: {'Enabled' if settings['daily_reports'] else 'Disabled'}\n" +
                          f"Weekly Reports: {'Enabled' if settings['weekly_reports'] else 'Disabled'}\n" +
                          f"Instant Alerts: {'Enabled' if settings['instant_alerts'] else 'Disabled'}")
    
    def load_recent_reports(self):
        """Load recent reports information"""
        recent_info = f"""
RECENT EMAIL ACTIVITY
====================
Last Daily Report: Not sent yet
Last Weekly Report: Not sent yet
Last Alert: Not sent yet

CONFIGURATION STATUS:
Email configured: {'Yes' if hasattr(self.email_notifier, 'sender_email') else 'No'}
SMTP Server: {getattr(self.email_notifier, 'smtp_server', 'Not set')}
SMTP Port: {getattr(self.email_notifier, 'smtp_port', 'Not set')}

ATTENDANCE SUMMARY:
Total people registered: {len(self.attendance_manager.get_attendance_stats().get('attendance_by_person', {}))}
Today's attendance: {self.attendance_manager.get_attendance_stats(days=1).get('total_attendances', 0)}
        """
        
        self.recent_reports.insert(1.0, recent_info)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EmailNotificationGUI()
    app.run()
