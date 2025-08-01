# Entry point for Face Recognition Attendance System
# Uses Tkinter for GUI


import os
import tkinter as tk
from tkinter import messagebox
from face_recognition_module import FaceRecognitionModule
from attendance_manager import AttendanceManager

# ...existing code...

def main():
    root = tk.Tk()
    root.title("Face Recognition Attendance System")
    root.configure(bg="#f0f4f8")
    root.geometry("420x540")

    main_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.RIDGE)
    main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Logo (if logo.png exists)
    try:
        from PIL import Image, ImageTk
        logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((80, 80))
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(main_frame, image=logo_photo, bg="#ffffff")
            logo_label.image = logo_photo  # Keep a reference
            logo_label.pack(pady=(10, 0))
    except Exception as e:
        print(f"Logo not loaded: {e}")

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


    # Title label
    title_label = tk.Label(main_frame, text="Face Recognition Attendance System", font=("Segoe UI", 15, "bold"), bg="#ffffff", fg="#2d3e50")
    title_label.pack(pady=(10, 10))

    # Date and time label
    datetime_label = tk.Label(main_frame, text="", font=("Segoe UI", 10), bg="#ffffff", fg="#4a4a4a")
    datetime_label.pack(pady=(0, 10))

    def update_datetime():
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datetime_label.config(text=f"Current Date & Time: {now}")
        root.after(1000, update_datetime)
    update_datetime()

    # Name entry
    name_label = tk.Label(main_frame, text="Name for Registration:", font=("Segoe UI", 11), bg="#ffffff", anchor="w")
    name_label.pack(fill=tk.X, padx=20)
    name_entry = tk.Entry(main_frame, font=("Segoe UI", 11), bd=2, relief=tk.GROOVE)
    name_entry.pack(padx=20, pady=(0, 10), fill=tk.X)
    register_btn = tk.Button(main_frame, text="Register Face", command=register_face, font=("Segoe UI", 10, "bold"), bg="#4caf50", fg="#fff", activebackground="#388e3c", bd=0, height=1)
    register_btn.pack(padx=20, pady=(0, 15), fill=tk.X)

    # Listbox for registered names
    reg_label = tk.Label(main_frame, text="Registered Names:", font=("Segoe UI", 11), bg="#ffffff", anchor="w")
    reg_label.pack(fill=tk.X, padx=20)
    listbox = tk.Listbox(main_frame, height=5, font=("Segoe UI", 10), bd=2, relief=tk.GROOVE, selectbackground="#90caf9")
    listbox.pack(padx=20, pady=(0, 5), fill=tk.X)
    delete_btn = tk.Button(main_frame, text="Delete Selected Face", command=delete_face, font=("Segoe UI", 10, "bold"), bg="#e53935", fg="#fff", activebackground="#b71c1c", bd=0, height=1)
    delete_btn.pack(padx=20, pady=(0, 15), fill=tk.X)

    # Attendance and export buttons
    start_btn = tk.Button(main_frame, text="Start Attendance", command=start_attendance, font=("Segoe UI", 10, "bold"), bg="#1976d2", fg="#fff", activebackground="#0d47a1", bd=0, height=1)
    start_btn.pack(padx=20, pady=(0, 10), fill=tk.X)
    export_btn = tk.Button(main_frame, text="Export to Excel", command=export_data, font=("Segoe UI", 10, "bold"), bg="#ffb300", fg="#fff", activebackground="#ff6f00", bd=0, height=1)
    export_btn.pack(padx=20, pady=(0, 10), fill=tk.X)
    clear_btn = tk.Button(main_frame, text="Clear All Registered Faces", command=clear_all_faces, font=("Segoe UI", 10, "bold"), bg="#fff", fg="#e53935", activebackground="#ffcdd2", bd=1, height=1)
    clear_btn.pack(padx=20, pady=(0, 10), fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    main()
