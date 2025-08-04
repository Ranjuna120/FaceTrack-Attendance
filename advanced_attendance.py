#!/usr/bin/env python3
"""
Enhanced Attendance Manager with advanced features
"""
import pandas as pd
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class AdvancedAttendanceManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.attendance_file = os.path.join(self.data_dir, "attendance.csv")
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.attendance_file):
            try:
                self.df = pd.read_csv(self.attendance_file)
                self.df['Date'] = pd.to_datetime(self.df['Time']).dt.date
                self.df['Time_Only'] = pd.to_datetime(self.df['Time']).dt.time
            except Exception:
                self.df = pd.DataFrame(columns=["Name", "Time", "Date", "Time_Only"])
        else:
            self.df = pd.DataFrame(columns=["Name", "Time", "Date", "Time_Only"])
    
    def mark_attendance(self, name, custom_time=None):
        """Mark attendance with optional custom time"""
        now = custom_time or datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        date_only = now.date()
        time_only = now.time()
        
        # Check if already marked today
        already_marked = ((self.df["Name"] == name) & (self.df["Date"] == date_only)).any()
        
        if not already_marked:
            new_row = pd.DataFrame([[name, time_str, date_only, time_only]], 
                                 columns=["Name", "Time", "Date", "Time_Only"])
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self.save_data()
            return True, f"Attendance marked for {name} at {time_str}"
        else:
            return False, f"Attendance already marked for {name} today."
    
    def save_data(self):
        """Save to both CSV and Excel"""
        self.df.to_csv(self.attendance_file, index=False)
        excel_file = os.path.join(self.data_dir, "attendance.xlsx")
        self.df.to_excel(excel_file, index=False)
    
    def get_attendance_stats(self, days=30):
        """Get attendance statistics for last N days"""
        if self.df.empty:
            return {}
        
        cutoff_date = datetime.now().date() - timedelta(days=days)
        recent_df = self.df[pd.to_datetime(self.df['Date']) >= pd.to_datetime(cutoff_date)]
        
        stats = {
            'total_attendances': len(recent_df),
            'unique_people': recent_df['Name'].nunique(),
            'daily_average': len(recent_df) / days,
            'most_punctual': recent_df.groupby('Name').size().idxmax() if not recent_df.empty else None,
            'attendance_by_person': recent_df['Name'].value_counts().to_dict(),
            'attendance_by_date': recent_df.groupby('Date').size().to_dict()
        }
        return stats
    
    def generate_report(self, output_file=None):
        """Generate detailed attendance report"""
        if self.df.empty:
            return "No attendance data available."
        
        output_file = output_file or os.path.join(self.data_dir, "attendance_report.txt")
        
        stats = self.get_attendance_stats()
        
        report = f"""
ATTENDANCE REPORT
================
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY (Last 30 days):
- Total Attendances: {stats['total_attendances']}
- Unique People: {stats['unique_people']}
- Daily Average: {stats['daily_average']:.1f}
- Most Regular: {stats['most_punctual']}

ATTENDANCE BY PERSON:
"""
        for name, count in stats['attendance_by_person'].items():
            report += f"- {name}: {count} days\n"
        
        report += "\nRECENT ATTENDANCE:\n"
        recent = self.df.tail(10)
        for _, row in recent.iterrows():
            report += f"- {row['Name']}: {row['Time']}\n"
        
        with open(output_file, 'w') as f:
            f.write(report)
        
        return f"Report saved to {output_file}"
    
    def create_attendance_chart(self):
        """Create attendance visualization"""
        if self.df.empty:
            return "No data to visualize"
        
        # Create a figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Attendance by person
        person_counts = self.df['Name'].value_counts()
        ax1.bar(person_counts.index, person_counts.values)
        ax1.set_title('Attendance Count by Person')
        ax1.set_xlabel('Person')
        ax1.set_ylabel('Days Attended')
        plt.setp(ax1.get_xticklabels(), rotation=45)
        
        # 2. Attendance over time
        daily_counts = self.df.groupby('Date').size()
        ax2.plot(daily_counts.index, daily_counts.values, marker='o')
        ax2.set_title('Daily Attendance Trend')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Number of People')
        plt.setp(ax2.get_xticklabels(), rotation=45)
        
        # 3. Attendance by hour
        self.df['Hour'] = pd.to_datetime(self.df['Time']).dt.hour
        hourly_counts = self.df['Hour'].value_counts().sort_index()
        ax3.bar(hourly_counts.index, hourly_counts.values)
        ax3.set_title('Attendance by Hour of Day')
        ax3.set_xlabel('Hour')
        ax3.set_ylabel('Count')
        
        # 4. Attendance heatmap (person vs date)
        pivot_data = self.df.pivot_table(index='Name', columns='Date', aggfunc='size', fill_value=0)
        sns.heatmap(pivot_data, ax=ax4, cmap='YlOrRd', cbar_kws={'label': 'Attended'})
        ax4.set_title('Attendance Heatmap')
        
        plt.tight_layout()
        chart_file = os.path.join(self.data_dir, "attendance_chart.png")
        plt.savefig(chart_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        return f"Chart saved to {chart_file}"
