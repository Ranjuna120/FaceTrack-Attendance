#!/usr/bin/env python3
"""
Utility functions for Face Recognition Attendance System
"""

import os
import sys
import traceback
from datetime import datetime

def log_error(error_msg, exception=None):
    """Log errors to console and file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_msg = f"[{timestamp}] ERROR: {error_msg}"
    if exception:
        log_msg += f"\nException: {str(exception)}\n{traceback.format_exc()}"
    
    print(log_msg)
    
    # Also log to file
    try:
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, "error.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_msg + "\n\n")
    except:
        pass  # Don't fail if we can't write to log file

def log_info(info_msg):
    """Log info messages."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] INFO: {info_msg}"
    print(log_msg)

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = {
        'cv2': 'opencv-python',
        'face_recognition': 'face_recognition',
        'pandas': 'pandas',
        'openpyxl': 'openpyxl'
    }
    
    missing_packages = []
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        error_msg = f"Missing required packages: {', '.join(missing_packages)}"
        error_msg += f"\nInstall with: pip install {' '.join(missing_packages)}"
        log_error(error_msg)
        return False
    
    return True

def validate_name(name):
    """Validate that a name is suitable for file naming."""
    if not name or not name.strip():
        return False, "Name cannot be empty"
    
    name = name.strip()
    
    # Check for invalid characters
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        if char in name:
            return False, f"Name cannot contain '{char}'"
    
    # Check length
    if len(name) > 50:
        return False, "Name too long (max 50 characters)"
    
    return True, name

def get_camera_indices():
    """Get list of available camera indices."""
    import cv2
    
    available_cameras = []
    for i in range(10):  # Check first 10 indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    
    return available_cameras

def format_file_size(size_bytes):
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def cleanup_temp_files(data_dir="data"):
    """Clean up any temporary files."""
    if not os.path.exists(data_dir):
        return
    
    temp_extensions = ['.tmp', '.temp', '.bak']
    
    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        _, ext = os.path.splitext(file)
        
        if ext.lower() in temp_extensions:
            try:
                os.remove(file_path)
                log_info(f"Cleaned up temp file: {file}")
            except Exception as e:
                log_error(f"Failed to cleanup {file}", e)
