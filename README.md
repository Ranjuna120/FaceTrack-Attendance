
<p align="center">
  <img src="logo.png" alt="FaceTrack-Attendance Logo" width="100"/>
</p>

# FaceTrack-Attendance

> A modern, user-friendly Face Recognition Attendance System built with Python, OpenCV, and Tkinter.

---

## 🚀 Features

- 🎥 **Face Registration & Recognition** using your webcam
- 📝 **Automatic Attendance Marking** with date and time
- 📋 **Export Attendance** to Excel (`attendance.xlsx`)
- 🧑‍💼 **Manage Registered Faces** (add, delete, clear all)
- 🖼️ **Custom Logo Support**
- 💡 **Modern, Clean UI** with Tkinter
- 🛡️ **Robust Error Handling**

---

## 📦 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

**Main dependencies:**
- opencv-python
- face_recognition
- pandas
- openpyxl
- pillow

---

## 🛠️ Usage

1. **Run the application:**
   ```bash
   python main.py
   ```
2. **Register Faces:** Enter a name and click `Register Face` (ensure your webcam is connected).
3. **Start Attendance:** Click `Start Attendance` to recognize faces and mark attendance.
4. **Export Data:** Click `Export to Excel` to save attendance to `data/attendance.xlsx`.
5. **Manage Faces:** Delete individual faces or clear all registered faces as needed.

---

## 📁 Project Structure

```
FaceTrack-Attendance/
│
├── main.py                  # Main GUI application
├── face_recognition_module.py # Face registration/recognition logic
├── attendance_manager.py    # Attendance marking and export
├── logger.py                # Centralized logging
├── config.py                # Configuration
├── utils.py                 # Utility functions
├── requirements.txt         # Python dependencies
├── logo.png                 # (Optional) App logo
├── data/                    # Attendance data (Excel/CSV)
└── ...
```

---

## 🙏 Credits

- [OpenCV](https://opencv.org/)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [Tkinter](https://wiki.python.org/moin/TkInter)
- [Pandas](https://pandas.pydata.org/)
- [Pillow](https://python-pillow.org/)

---

## 📜 License

This project is for educational purposes. Feel free to use and modify!
