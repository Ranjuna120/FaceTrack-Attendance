
<p align="center">
  <img src="logo.png" alt="FaceTrack-Attendance Logo" width="100"/>
</p>

# FaceTrack-Attendance

> A comprehensive, AI-powered Face Recognition Attendance System with advanced analytics, web dashboard, email notifications, and database management.

---

## 🚀 Key Features

### 🎯 **Core Attendance System**
- 🎥 **Advanced Face Registration & Recognition** using state-of-the-art AI
- 📝 **Real-time Attendance Marking** with precise timestamps
- 📊 **Smart Analytics & Statistics** with visual charts
- 🗄️ **SQLite Database Integration** for reliable data storage
- 📋 **Multiple Export Formats** (Excel, CSV, PDF reports)

### 🌐 **Web Interface & API**
- 🖥️ **Modern Web Dashboard** with live attendance tracking
- � **REST API** for mobile app integration
- 📱 **Responsive Design** works on all devices
- 🔐 **Secure Authentication** with JWT tokens

### 📧 **Email Notifications**
- 📨 **Automated Daily Reports** sent via email
- ⚡ **Instant Attendance Alerts** for real-time notifications
- 📑 **Weekly Summary Reports** with Excel attachments
- ⏰ **Customizable Scheduling** for automated emails

### 🎛️ **Advanced Management**
- �️ **Master Control Panel** - unified interface for all features
- 👥 **User Management System** with role-based access
- � **Advanced Analytics** with charts and visualizations
- 🔧 **Configuration Management** with easy-to-use GUIs

---

## 📦 Installation & Setup

### 🔧 **Quick Setup**
```bash
# Clone the repository
git clone https://github.com/Ranjuna120/FaceTrack-Attendance.git
cd FaceTrack-Attendance

# Install dependencies
pip install -r requirements.txt

# Run the main application
python main.py
```

### 📋 **Dependencies**
**Core Libraries:**
- opencv-python (Computer Vision)
- face_recognition (AI Face Recognition)
- pandas (Data Management)
- openpyxl (Excel Export)
- pillow (Image Processing)

**Advanced Features:**
- flask, flask-cors (Web Dashboard)
- matplotlib, seaborn (Analytics & Charts)
- sqlite3 (Database - Built into Python)
- smtplib (Email Notifications)
- PyJWT (API Authentication)

**Install all at once:**
```bash
pip install -r requirements.txt
```

---

## 🎯 **Usage Guide**

### 🚀 **Method 1: Main GUI Application**
```bash
python main.py
```
- **Basic face registration and attendance**
- **Excel export functionality**
- **Simple, user-friendly interface**

### 🎛️ **Method 2: Master Control Panel** (Recommended)
```bash
python master_control.py
```
- **Complete system management**
- **Access to all advanced features**
- **Analytics, database, email, web dashboard**
- **Multi-tab interface for easy navigation**

### 🌐 **Method 3: Web Dashboard**
```bash
python web_dashboard.py
```
- **Modern web interface**
- **Real-time attendance tracking**
- **Visual analytics and charts**
- **Access via browser: `http://localhost:5000`**

### 📧 **Method 4: Email Notifications**
```bash
python email_config_gui.py
```
- **Configure email settings**
- **Test email functionality**
- **Schedule automated reports**
- **Send instant alerts**

### 🔗 **Method 5: REST API Server**
```bash
python api_server.py
```
- **RESTful API for mobile apps**
- **JSON data exchange**
- **Secure authentication**
- **API endpoints for all features**

---

## 📚 **Feature Detailed Guide**

### 🎯 **1. Face Registration & Recognition**
**Step-by-Step:**
1. Open any interface (main.py, master_control.py, or web dashboard)
2. **Register Faces:** 
   - Enter person's name
   - Click "Register Face"
   - Position face in the green detection box
   - Press SPACE to capture, ESC to cancel
   - Ensure good lighting and clear face visibility

3. **Start Attendance:**
   - Click "Start Attendance" 
   - System will recognize registered faces automatically
   - Press 'q' to stop recognition
   - Attendance is marked with precise timestamp

### 📊 **2. Advanced Analytics** 
**Access via Master Control Panel:**
- **Daily/Weekly/Monthly Statistics**
- **Attendance Trends with Visual Charts**
- **Person-wise Attendance Reports**
- **Export Analytics as PDF/Excel**

### 🗄️ **3. Database Management**
**Automatic SQLite Integration:**
- **User Management** - Add, edit, delete users
- **Attendance History** - Complete attendance records
- **Data Backup & Restore** functionality
- **Query-based Reports** for specific date ranges

### 📧 **4. Email Notifications Setup**
**For Gmail Users:**
1. **Enable 2-Factor Authentication** in Google Account
2. **Generate App Password:**
   - Google Account → Security → 2-Step Verification
   - App passwords → Generate for "Mail"
   - Use this 16-character password (not your regular password)

3. **Configure in Email GUI:**
   ```bash
   python email_config_gui.py
   ```
   - Enter email and app password
   - Test connection
   - Schedule reports (Daily/Weekly/Instant alerts)

**Available Email Features:**
- 📨 **Daily Reports** - Automatic attendance summaries
- ⚡ **Instant Alerts** - Real-time attendance notifications  
- 📊 **Weekly Summaries** - Comprehensive reports with Excel attachments
- ⏰ **Custom Scheduling** - Set preferred times

### 🌐 **5. Web Dashboard Features**
**Access:** `http://localhost:5000` after running `python web_dashboard.py`

- **Live Attendance Tracking**
- **Interactive Charts & Analytics** 
- **User Management Interface**
- **Export Functionality**
- **Mobile-Responsive Design**

### 🔗 **6. REST API Integration**
**Start API Server:** `python api_server.py`

**Available Endpoints:**
- `POST /api/register` - Register new user
- `POST /api/attendance` - Mark attendance
- `GET /api/users` - Get all users
- `GET /api/attendance` - Get attendance records
- `GET /api/stats` - Get attendance statistics

**Example Usage:**
```bash
# Register user
curl -X POST http://localhost:5001/api/register \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe"}'

# Get attendance stats
curl http://localhost:5001/api/stats
```

---

## 🔧 **Troubleshooting & Configuration**

### ⚙️ **Common Configuration Options**
Edit `config.py` to customize:
```python
# Face Recognition Settings
FACE_RECOGNITION_TOLERANCE = 0.5  # 0.4 (strict) to 0.8 (lenient)
FACE_RECOGNITION_MODEL = "hog"     # "hog" (fast) or "cnn" (accurate)

# Camera Settings
CAMERA_INDEX = 0                   # Try 0, 1, 2 if camera not found
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Database Settings
DATABASE_PATH = "data/attendance.db"

# Email Settings (can also configure via GUI)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

### 🐛 **Common Issues & Solutions**

#### **Face Registration Problems**
**Issue:** "No face detected"
- ✅ **Solution:** Ensure good lighting, face clearly visible
- ✅ Remove glasses, masks, or head coverings temporarily
- ✅ Try different camera angles

**Issue:** "Multiple faces detected"  
- ✅ **Solution:** Ensure only one person in camera view
- ✅ Others should step out of frame during registration

#### **Face Recognition Problems**
**Issue:** "Face not recognized"
- ✅ **Solution:** Increase `FACE_RECOGNITION_TOLERANCE` in config.py
- ✅ Re-register face with better lighting
- ✅ Try different camera position

**Issue:** "Slow recognition performance"
- ✅ **Solution:** Change `FACE_RECOGNITION_MODEL` to "hog"
- ✅ Increase `FRAME_SKIP` value
- ✅ Reduce camera resolution

#### **Camera Issues**
**Issue:** "Camera not accessible"
- ✅ **Solution:** Close other apps using camera
- ✅ Try different `CAMERA_INDEX` values (0, 1, 2)
- ✅ Run as administrator
- ✅ Check camera permissions in Windows settings

#### **Email Issues**
**Issue:** "Authentication failed"
- ✅ **Solution:** Use App Password, not regular Gmail password
- ✅ Enable 2-Factor Authentication first
- ✅ Check email configuration in `email_config_gui.py`

**Issue:** "Connection failed"
- ✅ **Solution:** Verify SMTP settings (smtp.gmail.com, port 587)
- ✅ Check internet connection
- ✅ Try port 465 with SSL

#### **Database Issues**
**Issue:** "Database locked" or "Permission denied"
- ✅ **Solution:** Close all instances of the application
- ✅ Check if file is read-only
- ✅ Run as administrator

#### **Web Dashboard Issues**
**Issue:** "Port already in use"
- ✅ **Solution:** Change port in `web_dashboard.py`
- ✅ Kill existing processes: `taskkill /f /im python.exe`

### 🔧 **Performance Optimization**
**For Slower Computers:**
```python
# In config.py
FACE_RECOGNITION_MODEL = "hog"  # Faster but less accurate
FRAME_SKIP = 3                  # Skip frames for better performance
FACE_RECOGNITION_TOLERANCE = 0.6  # More lenient matching
```

**For Better Accuracy:**
```python
# In config.py  
FACE_RECOGNITION_MODEL = "cnn"  # More accurate but slower
FRAME_SKIP = 1                  # Process every frame
FACE_RECOGNITION_TOLERANCE = 0.4  # Stricter matching
```

---

## 📁 **Project Structure**

```
FaceTrack-Attendance/
│
├── 🎯 Core Application Files
│   ├── main.py                           # Main GUI application
│   ├── face_recognition_module.py        # AI face recognition logic
│   ├── attendance_manager.py             # Basic attendance management
│   └── config.py                         # Configuration settings
│
├── 🚀 Advanced Features
│   ├── master_control.py                 # Unified control panel
│   ├── simple_advanced_attendance.py     # Enhanced attendance system
│   ├── database_manager.py               # SQLite database management
│   ├── web_dashboard.py                  # Flask web interface
│   ├── api_server.py                     # REST API server
│   └── email_notifier.py                 # Email notification system
│
├── 🎛️ User Interfaces
│   ├── email_config_gui.py               # Email configuration GUI
│   └── logo.png                          # Application logo
│
├── 🧪 Testing & Demos
│   ├── test_all_features.py              # Comprehensive feature testing
│   ├── feature_demo.py                   # Feature demonstration
│   ├── quick_email_test.py               # Email testing utility
│   └── test_face_recognition_module.py   # Face recognition tests
│
├── 🔧 Utilities & Support
│   ├── logger.py                         # Centralized logging
│   ├── utils.py                          # Utility functions
│   ├── requirements.txt                  # Python dependencies
│   └── EMAIL_SETUP_GUIDE.md              # Email setup instructions
│
└── 📁 Data Directory
    ├── data/
    │   ├── attendance.xlsx                # Excel attendance records
    │   ├── attendance.db                  # SQLite database
    │   └── faces/                         # Stored face encodings (.npy files)
    └── __pycache__/                       # Python cache files
```

### 📊 **File Descriptions**

**🎯 Core Files:**
- `main.py` - Simple GUI for basic attendance functionality
- `face_recognition_module.py` - Core AI face recognition and registration
- `attendance_manager.py` - Basic attendance marking and Excel export
- `config.py` - System configuration and settings

**🚀 Advanced Features:**
- `master_control.py` - **Main interface** with all features in tabs
- `database_manager.py` - SQLite database operations and user management  
- `web_dashboard.py` - Modern web interface with Flask
- `api_server.py` - REST API for mobile app integration
- `email_notifier.py` - Automated email reports and alerts

**🧪 Testing & Demos:**
- `test_all_features.py` - Tests all system components
- `feature_demo.py` - Demonstrates advanced features
- `quick_email_test.py` - Simple email functionality test

**📁 Data Storage:**
- `data/attendance.xlsx` - Excel format attendance records
- `data/attendance.db` - SQLite database with user and attendance tables
- `data/faces/` - Directory containing face encoding files (.npy format)

---

## 🎉 **Quick Start Examples**

### 🚀 **Basic Usage (Beginners)**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start basic GUI
python main.py

# 3. Register your face, mark attendance, export to Excel
```

### 🎛️ **Advanced Usage (Recommended)**
```bash
# 1. Open Master Control Panel
python master_control.py

# 2. Access all features in one interface:
#    - Face Management
#    - Database Operations  
#    - Analytics & Charts
#    - Email Notifications
#    - Web Dashboard Control
```

### 🌐 **Web Interface**
```bash
# 1. Start web server
python web_dashboard.py

# 2. Open browser to: http://localhost:5000
# 3. Modern web interface with real-time updates
```

### 📧 **Email Notifications**
```bash
# 1. Configure email settings
python email_config_gui.py

# 2. Set up Gmail App Password (see EMAIL_SETUP_GUIDE.md)
# 3. Test and schedule automated reports
```

---

## 🔄 **System Integration Examples**

### 🏢 **For Organizations**
1. **Setup:** Run `master_control.py` for admin interface
2. **Register:** Add all employees using face registration
3. **Deploy:** Use `web_dashboard.py` for public access terminals  
4. **Monitor:** Enable email notifications for HR team
5. **Reports:** Generate automated daily/weekly attendance reports

### 📱 **For Mobile App Integration**
1. **API Server:** Start `python api_server.py`  
2. **Endpoints:** Use REST API endpoints for mobile app
3. **Authentication:** Implement JWT token-based security
4. **Real-time:** WebSocket support for live updates

### 🏠 **For Small Teams/Home Use**
1. **Simple Setup:** Use `main.py` for basic functionality
2. **Quick Start:** Register faces and start marking attendance
3. **Export:** Regular Excel exports for record keeping

---

## 📈 **Advanced Analytics Features**

### 📊 **Available Reports**
- **Daily Attendance Summary** - Who attended today
- **Weekly/Monthly Trends** - Attendance patterns over time  
- **Person-wise Statistics** - Individual attendance records
- **Peak Hours Analysis** - Most active attendance times
- **Absence Reports** - Who missed attendance

### 📉 **Visual Charts**
- **Attendance Trends** - Line charts showing patterns
- **Daily Distribution** - Bar charts of daily attendance
- **Person Comparison** - Comparative attendance statistics
- **Time-based Analysis** - Heatmaps of attendance timing

### 📋 **Export Options**
- **Excel Files** - Complete attendance data with formatting
- **PDF Reports** - Professional formatted reports
- **CSV Data** - Raw data for external analysis
- **Email Reports** - Automated delivery to stakeholders

---

## 🛡️ **Security Features**

### 🔐 **Authentication & Access Control**
- **JWT Token-based API Authentication**
- **Role-based Access Control** (Admin, User, Viewer)
- **Secure Password Handling** for email configurations
- **Session Management** for web interface

### 🛡️ **Data Protection**
- **SQLite Database Encryption** options
- **Secure Face Encoding Storage** (.npy files)
- **HTTPS Support** for web dashboard (configurable)
- **Email SSL/TLS Encryption** for notifications

### 📊 **Privacy Compliance**
- **Local Data Storage** - No cloud dependency
- **Face Encoding Storage** - Mathematical representations, not images
- **Data Export/Deletion** capabilities for GDPR compliance
- **Audit Logging** for access tracking

---

## 🙏 **Credits & Acknowledgments**

### 🛠️ **Core Technologies**
- **[OpenCV](https://opencv.org/)** - Computer Vision and Camera Handling
- **[face_recognition](https://github.com/ageitgey/face_recognition)** - AI-powered Face Recognition
- **[Flask](https://flask.palletsprojects.com/)** - Web Framework for Dashboard
- **[Tkinter](https://wiki.python.org/moin/TkInter)** - GUI Framework
- **[SQLite](https://www.sqlite.org/)** - Embedded Database
- **[Pandas](https://pandas.pydata.org/)** - Data Analysis and Management

### 📊 **Visualization & Analytics**
- **[Matplotlib](https://matplotlib.org/)** - Statistical Charts and Graphs
- **[Seaborn](https://seaborn.pydata.org/)** - Advanced Statistical Visualization
- **[Pillow](https://python-pillow.org/)** - Image Processing

### 📧 **Communication & Integration**
- **[smtplib](https://docs.python.org/3/library/smtplib.html)** - Email Integration
- **[PyJWT](https://pyjwt.readthedocs.io/)** - API Authentication
- **[Flask-CORS](https://flask-cors.readthedocs.io/)** - Cross-Origin Resource Sharing

---

## 📜 **License & Usage**

### 📄 **License**
This project is released under the **MIT License** - feel free to use, modify, and distribute!

### 🎓 **Educational Use**
- ✅ Perfect for **learning computer vision and AI**
- ✅ Great **portfolio project** for students
- ✅ **Open source** - examine and learn from the code

### 🏢 **Commercial Use**
- ✅ **Free for commercial use** with proper attribution
- ✅ **Customizable** for specific business needs
- ✅ **Scalable** - can be adapted for large organizations

### 🤝 **Contributing**
We welcome contributions! Please:
1. **Fork the repository**
2. **Create a feature branch**
3. **Submit a pull request**
4. **Follow the existing code style**

---

## 📞 **Support & Contact**

### 🐛 **Bug Reports**
- **GitHub Issues:** [Report bugs here](https://github.com/Ranjuna120/FaceTrack-Attendance/issues)
- **Include:** Error messages, system info, steps to reproduce

### 💡 **Feature Requests**  
- **GitHub Discussions:** [Suggest new features](https://github.com/Ranjuna120/FaceTrack-Attendance/discussions)
- **Describe:** What you need and why it would be useful

### 📚 **Documentation**
- **README.md** - This comprehensive guide
- **EMAIL_SETUP_GUIDE.md** - Detailed email configuration
- **Built-in Help** - Available in all GUI applications

---

## 🎯 **What's New in Latest Version**

### ✨ **Version 2.0 Features**
- 🆕 **Master Control Panel** - Unified interface for all features
- 🆕 **SQLite Database Integration** - Reliable data storage
- 🆕 **Web Dashboard** - Modern browser-based interface  
- 🆕 **Email Notifications** - Automated reports and alerts
- 🆕 **REST API** - Mobile app integration capabilities
- 🆕 **Advanced Analytics** - Charts and visual reports
- 🆕 **Multi-interface Support** - GUI, Web, API, CLI options

### 🔧 **Improvements**
- 🔧 **Enhanced Face Recognition** - Better accuracy and speed
- 🔧 **Improved Error Handling** - More user-friendly error messages
- 🔧 **Better Configuration** - Easy customization options
- 🔧 **Performance Optimization** - Faster processing and response times

**🎉 Your FaceTrack-Attendance system is now a comprehensive, enterprise-ready solution!**
