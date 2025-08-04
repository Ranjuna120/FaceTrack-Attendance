#!/usr/bin/env python3
"""
Email notification system for attendance
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
import pandas as pd
import os

class EmailNotifier:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = None
        self.sender_password = None
        
    def configure(self, sender_email, sender_password):
        """Configure email credentials"""
        self.sender_email = sender_email
        self.sender_password = sender_password
        
    def send_daily_report(self, recipient_email, attendance_data):
        """Send daily attendance report"""
        if not self.sender_email or not self.sender_password:
            return False, "Email not configured"
        
        # Create message
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = f"Daily Attendance Report - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Create HTML body
        html_body = f"""
        <html>
        <body>
            <h2>Daily Attendance Report</h2>
            <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
            <p><strong>Total Attendance:</strong> {len(attendance_data)}</p>
            
            <h3>Attendance Details:</h3>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #f2f2f2;">
                    <th style="padding: 10px;">Name</th>
                    <th style="padding: 10px;">Time</th>
                </tr>
        """
        
        for _, row in attendance_data.iterrows():
            html_body += f"""
                <tr>
                    <td style="padding: 10px;">{row['Name']}</td>
                    <td style="padding: 10px;">{row['Time']}</td>
                </tr>
            """
        
        html_body += """
            </table>
            <br>
            <p><em>This is an automated report from FaceTrack Attendance System.</em></p>
        </body>
        </html>
        """
        
        message.attach(MIMEText(html_body, "html"))
        
        try:
            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            return True, "Email sent successfully"
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"
    
    def send_attendance_alert(self, recipient_email, person_name):
        """Send immediate attendance alert"""
        if not self.sender_email or not self.sender_password:
            return False, "Email not configured"
        
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = f"Attendance Alert - {person_name}"
        
        body = f"""
        <html>
        <body>
            <h2>Attendance Alert</h2>
            <p><strong>{person_name}</strong> has been marked present.</p>
            <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <br>
            <p><em>This is an automated alert from FaceTrack Attendance System.</em></p>
        </body>
        </html>
        """
        
        message.attach(MIMEText(body, "html"))
        
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            return True, "Alert sent successfully"
        except Exception as e:
            return False, f"Failed to send alert: {str(e)}"
    
    def send_weekly_summary(self, recipient_email, attendance_summary):
        """Send weekly attendance summary"""
        if not self.sender_email or not self.sender_password:
            return False, "Email not configured"
        
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = f"Weekly Attendance Summary - Week of {datetime.now().strftime('%Y-%m-%d')}"
        
        # Attach Excel file if provided
        if isinstance(attendance_summary, str) and attendance_summary.endswith('.xlsx'):
            with open(attendance_summary, "rb") as attachment:
                part = MimeBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attendance_summary)}'
                )
                message.attach(part)
        
        body = f"""
        <html>
        <body>
            <h2>Weekly Attendance Summary</h2>
            <p><strong>Week of:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
            <p>Please find the detailed attendance report attached.</p>
            <br>
            <p><em>This is an automated report from FaceTrack Attendance System.</em></p>
        </body>
        </html>
        """
        
        message.attach(MIMEText(body, "html"))
        
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            return True, "Weekly summary sent successfully"
        except Exception as e:
            return False, f"Failed to send weekly summary: {str(e)}"
