# Entry point for Face Recognition Attendance System
# Uses Tkinter for GUI

import tkinter as tk
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

    def start_attendance():
        recognized = face_module.recognize_faces()
        for name in recognized:
            attendance_manager.mark_attendance(name)

    def export_data():
        attendance_manager.export_to_excel()

    tk.Label(root, text="Name for Registration:").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()
    tk.Button(root, text="Register Face", command=register_face).pack(pady=5)
    tk.Button(root, text="Start Attendance", command=start_attendance).pack(pady=5)
    tk.Button(root, text="Export to Excel", command=export_data).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
