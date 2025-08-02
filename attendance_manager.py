# Manages attendance marking and data export
import pandas as pd
import os

class AttendanceManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.attendance_file = os.path.join(self.data_dir, "attendance.csv")
        if os.path.exists(self.attendance_file):
            try:
                self.df = pd.read_csv(self.attendance_file, dtype={"Name": str, "Time": str})
                if not set(["Name", "Time"]).issubset(self.df.columns):
                    self.df = pd.DataFrame(columns=["Name", "Time"])
            except Exception:
                self.df = pd.DataFrame(columns=["Name", "Time"])
        else:
            self.df = pd.DataFrame(columns=["Name", "Time"])

    def mark_attendance(self, name):
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.df.empty or not set(["Name", "Time"]).issubset(self.df.columns):
            self.df = pd.DataFrame(columns=["Name", "Time"])
        self.df["Name"] = self.df["Name"].astype(str)
        self.df["Time"] = self.df["Time"].astype(str)
        already_marked = ((self.df["Name"] == name) & (self.df["Time"].str[:10] == now[:10])).any()
        if not already_marked:
            new_row = pd.DataFrame([[name, now]], columns=["Name", "Time"])
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self.df.to_csv(self.attendance_file, index=False)
            excel_file = os.path.join(self.data_dir, "attendance.xlsx")
            self.df.to_excel(excel_file, index=False)
            print(f"Attendance marked for {name}")
        else:
            print(f"Attendance already marked for {name} today.")

    def export_to_excel(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        excel_file = os.path.join(self.data_dir, "attendance.xlsx")
        self.df.to_excel(excel_file, index=False)
        print(f"Attendance exported to {excel_file}")
