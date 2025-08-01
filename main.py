# Entry point for Face Recognition Attendance System
# Uses Tkinter for GUI

import tkinter as tk
from tkinter import messagebox
from face_recognition_module import FaceRecognitionModule
from attendance_manager import AttendanceManager

# ...existing code...

def main():
    import os

    def clear_all_faces():
        if messagebox.askyesno("Clear All Faces", "Are you sure you want to delete all registered faces? This cannot be undone."):
            data_dir = getattr(face_module, 'data_dir', 'data')
            removed = 0
            for file in os.listdir(data_dir):
                if file.endswith('.npy'):
                    try:
                        os.remove(os.path.join(data_dir, file))
                        removed += 1
                    except Exception as e:
                        print(f"Failed to delete {file}: {e}")
            registered_names.clear()
            update_listbox()
            messagebox.showinfo("Clear All Faces", f"Deleted {removed} face data file(s).")
    root = tk.Tk()
    root.title("Face Recognition Attendance System")

    face_module = FaceRecognitionModule()
    attendance_manager = AttendanceManager()

    # List to store registered names
    registered_names = []

    def update_listbox():
        listbox.delete(0, tk.END)
        for n in registered_names:
            listbox.insert(tk.END, n)

    def register_face():
        name = name_entry.get()
        if name:
            try:
                success, msg = face_module.register_face(name)
                if success:
                    if name not in registered_names:
                        registered_names.append(name)
                        update_listbox()
                    messagebox.showinfo("Success", msg)
                else:
                    messagebox.showwarning("Registration Failed", msg)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to register face: {e}")
        else:
            messagebox.showwarning("Input Error", "Please enter a name to register.")

    def start_attendance():
        try:
            recognized = face_module.recognize_faces()
            if recognized:
                for name in recognized:
                    attendance_manager.mark_attendance(name)
                messagebox.showinfo("Attendance", f"Attendance marked for: {', '.join(recognized)}")
            else:
                messagebox.showinfo("Attendance", "No faces recognized.")
        except Exception as e:
            messagebox.showerror("Camera Error", f"Failed to access camera: {e}")

    def export_data():
        if messagebox.askyesno("Export", "Are you sure you want to export attendance to Excel?"):
            try:
                attendance_manager.export_to_excel()
                messagebox.showinfo("Export", "Attendance exported to Excel.")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {e}")

    def delete_face():
        selected = listbox.curselection()
        if selected:
            name = listbox.get(selected[0])
            # You should implement delete_face in FaceRecognitionModule for this to work
            try:
                face_module.delete_face(name)
                registered_names.remove(name)
                update_listbox()
                messagebox.showinfo("Delete", f"Deleted face data for {name}")
            except Exception as e:
                messagebox.showerror("Delete Error", f"Failed to delete: {e}")
        else:
            messagebox.showwarning("Delete", "Select a name to delete.")


    # Date and time label
    datetime_label = tk.Label(root, text="", font=("Arial", 10))
    datetime_label.pack(pady=2)

    def update_datetime():
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datetime_label.config(text=f"Current Date & Time: {now}")
        root.after(1000, update_datetime)
    update_datetime()

    tk.Label(root, text="Name for Registration:").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()
    tk.Button(root, text="Register Face", command=register_face).pack(pady=5)

    # Listbox for registered names
    tk.Label(root, text="Registered Names:").pack()
    listbox = tk.Listbox(root, height=5)
    listbox.pack(pady=2)
    tk.Button(root, text="Delete Selected Face", command=delete_face).pack(pady=2)


    tk.Button(root, text="Start Attendance", command=start_attendance).pack(pady=5)
    tk.Button(root, text="Export to Excel", command=export_data).pack(pady=5)
    tk.Button(root, text="Clear All Registered Faces", command=clear_all_faces, fg="red").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
