# Entry point for Face Recognition Attendance System
# Uses Tkinter for GUI

import tkinter as tk
from tkinter import messagebox
from face_recognition_module import FaceRecognitionModule
from attendance_manager import AttendanceManager

# ...existing code...

def main():
    root = tk.Tk()
    root.title("Face Recognition Attendance System")

    face_module = FaceRecognitionModule()
    attendance_manager = AttendanceManager()

    def register_face():
        name = name_entry.get()
        if name:
            face_module.register_face(name)
            messagebox.showinfo("Success", f"Face registered for {name}")
        else:
            messagebox.showwarning("Input Error", "Please enter a name to register.")

    def start_attendance():
        recognized = face_module.recognize_faces()
        if recognized:
            for name in recognized:
                attendance_manager.mark_attendance(name)
            messagebox.showinfo("Attendance", f"Attendance marked for: {', '.join(recognized)}")
        else:
            messagebox.showinfo("Attendance", "No faces recognized.")

    def export_data():
        attendance_manager.export_to_excel()
        messagebox.showinfo("Export", "Attendance exported to Excel.")

    tk.Label(root, text="Name for Registration:").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()
    tk.Button(root, text="Register Face", command=register_face).pack(pady=5)
    tk.Button(root, text="Start Attendance", command=start_attendance).pack(pady=5)
    tk.Button(root, text="Export to Excel", command=export_data).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
