# Manages attendance marking and data export
import pandas as pd
import os

class AttendanceManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.attendance_file = os.path.join(data_dir, "attendance.csv")
        if os.path.exists(self.attendance_file):
            self.df = pd.read_csv(self.attendance_file)
        else:
            self.df = pd.DataFrame(columns=["Name", "Time"])

    def mark_attendance(self, name):
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not ((self.df["Name"] == name) & (self.df["Time"].str[:10] == now[:10])).any():
            self.df = pd.concat([self.df, pd.DataFrame([[name, now]], columns=["Name", "Time"])], ignore_index=True)
            self.df.to_csv(self.attendance_file, index=False)
            print(f"Attendance marked for {name}")
        else:
            print(f"Attendance already marked for {name} today.")

    def export_to_excel(self):
        excel_file = os.path.join(self.data_dir, "attendance.xlsx")
        self.df.to_excel(excel_file, index=False)
        print(f"Attendance exported to {excel_file}")
