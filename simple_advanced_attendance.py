#!/usr/bin/env python3
"""
Simplified Advanced Attendance Manager - Compatible Version
"""
import pandas as pd
import os
from datetime import datetime, timedelta

class SimpleAdvancedAttendanceManager:
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
                # Ensure we have the required columns
                if 'Time' in self.df.columns:
                    self.df['Date'] = pd.to_datetime(self.df['Time']).dt.date
                    self.df['Time_Only'] = pd.to_datetime(self.df['Time']).dt.time
                else:
                    self.df = pd.DataFrame(columns=["Name", "Time", "Date", "Time_Only"])
            except Exception as e:
                print(f"Error loading data: {e}")
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
        if not self.df.empty and 'Date' in self.df.columns:
            already_marked = ((self.df["Name"] == name) & (self.df["Date"] == date_only)).any()
        else:
            already_marked = False
        
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
        try:
            self.df.to_csv(self.attendance_file, index=False)
            excel_file = os.path.join(self.data_dir, "attendance.xlsx")
            self.df.to_excel(excel_file, index=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def get_attendance_stats(self, days=30):
        """Get attendance statistics for last N days"""
        if self.df.empty:
            return {
                'total_attendances': 0,
                'unique_people': 0,
                'daily_average': 0,
                'most_punctual': None,
                'attendance_by_person': {},
                'attendance_by_date': {}
            }
        
        try:
            cutoff_date = datetime.now().date() - timedelta(days=days)
            if 'Date' in self.df.columns:
                recent_df = self.df[pd.to_datetime(self.df['Date']) >= pd.to_datetime(cutoff_date)]
            else:
                recent_df = self.df
            
            if recent_df.empty:
                return {
                    'total_attendances': 0,
                    'unique_people': 0,
                    'daily_average': 0,
                    'most_punctual': None,
                    'attendance_by_person': {},
                    'attendance_by_date': {}
                }
            
            stats = {
                'total_attendances': len(recent_df),
                'unique_people': recent_df['Name'].nunique(),
                'daily_average': len(recent_df) / days,
                'most_punctual': recent_df['Name'].value_counts().index[0] if len(recent_df) > 0 else None,
                'attendance_by_person': recent_df['Name'].value_counts().to_dict(),
                'attendance_by_date': recent_df.groupby('Date').size().to_dict() if 'Date' in recent_df.columns else {}
            }
            return stats
        except Exception as e:
            print(f"Error calculating stats: {e}")
            return {
                'total_attendances': 0,
                'unique_people': 0,
                'daily_average': 0,
                'most_punctual': None,
                'attendance_by_person': {},
                'attendance_by_date': {}
            }
    
    def generate_report(self, output_file=None):
        """Generate detailed attendance report"""
        if self.df.empty:
            return "No attendance data available."
        
        output_file = output_file or os.path.join(self.data_dir, "attendance_report.txt")
        
        try:
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
        except Exception as e:
            return f"Error generating report: {e}"
    
    def create_simple_chart(self):
        """Create a simple text-based chart"""
        if self.df.empty:
            return "No data to visualize"
        
        try:
            # Simple text-based visualization
            stats = self.get_attendance_stats()
            chart_text = f"""
ATTENDANCE CHART (Text Version)
==============================

Attendance by Person:
"""
            for name, count in stats['attendance_by_person'].items():
                bar = "#" * min(count, 20)  # Max 20 characters, using # instead of unicode
                chart_text += f"{name:15} |{bar} ({count})\n"
            
            chart_file = os.path.join(self.data_dir, "attendance_chart.txt")
            with open(chart_file, 'w', encoding='utf-8') as f:
                f.write(chart_text)
            
            print(chart_text)
            return f"Simple chart saved to {chart_file}"
        except Exception as e:
            return f"Error creating chart: {e}"

# Test the simplified version
if __name__ == "__main__":
    print("Testing Simplified Advanced Attendance Manager...")
    
    # Initialize manager
    manager = SimpleAdvancedAttendanceManager()
    
    # Test marking attendance
    success, message = manager.mark_attendance("TestUser")
    print(f"Mark attendance: {message}")
    
    # Get statistics
    stats = manager.get_attendance_stats()
    print("\nCurrent Statistics:")
    print(f"Total Attendances: {stats['total_attendances']}")
    print(f"Unique People: {stats['unique_people']}")
    print(f"Attendance by Person: {stats['attendance_by_person']}")
    
    # Generate report
    report_result = manager.generate_report()
    print(f"\nReport: {report_result}")
    
    # Create simple chart
    chart_result = manager.create_simple_chart()
    print(f"\nChart: {chart_result}")
    
    print("\nTest completed successfully!")
