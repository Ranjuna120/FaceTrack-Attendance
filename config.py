# Enhanced Configuration for FaceTrack-Attendance

# Directory settings
DATA_DIR = "data"
EXCEL_FILE = "data/attendance.xlsx"

# Face recognition settings
FACE_RECOGNITION_TOLERANCE = 0.6  # Lower = more strict, Higher = more lenient
FACE_RECOGNITION_MODEL = "hog"    # "hog" for speed, "cnn" for accuracy
NUM_JITTERS = 1                   # Reduced from 3 for compatibility
ENCODING_MODEL = "small"          # "small" or "large" - small is more compatible
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Recognition timeout (frames)
RECOGNITION_TIMEOUT_FRAMES = 300  # ~10 seconds at 30 FPS
FRAME_SKIP = 3                    # Process every 3rd frame for performance

# Database settings
DATABASE_PATH = "data/attendance.db"
BACKUP_ENABLED = True
BACKUP_INTERVAL_DAYS = 7

# Email notification settings
EMAIL_ENABLED = False
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = ""  # Configure this
SENDER_PASSWORD = ""  # Configure this or use app password
ADMIN_EMAIL = ""  # Configure this

# Auto-reporting settings
DAILY_REPORT_ENABLED = False
DAILY_REPORT_TIME = "18:00"  # 6 PM
WEEKLY_REPORT_ENABLED = False
WEEKLY_REPORT_DAY = "sunday"

# Security settings
SESSION_TIMEOUT_MINUTES = 60
MAX_LOGIN_ATTEMPTS = 5
REQUIRE_AUTHENTICATION = False

# Advanced features
MULTIPLE_FACE_DETECTION = True
ANTI_SPOOFING_ENABLED = False  # Requires additional libraries
LOCATION_TRACKING = False
TEMPERATURE_CHECKING = False

# UI settings
THEME = "light"  # "light" or "dark"
LANGUAGE = "en"  # "en", "si", etc.
SHOW_CONFIDENCE_SCORES = False

# Performance settings
MAX_FACE_ENCODINGS_CACHE = 100
IMAGE_PROCESSING_THREADS = 2
AUTO_CLEANUP_ENABLED = True
CLEANUP_INTERVAL_DAYS = 30

# Logging settings
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE = True
MAX_LOG_SIZE_MB = 10
LOG_RETENTION_DAYS = 30

# Integration settings
API_ENABLED = True
API_PORT = 5001
WEB_DASHBOARD_ENABLED = True
WEB_DASHBOARD_PORT = 5000
MOBILE_APP_SUPPORT = True
