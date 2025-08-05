#!/usr/bin/env python3
"""
Setup script to check and install requirements for Face Recognition Attendance System
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required!")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")
    
    requirements = [
        "opencv-python",
        "face_recognition",
        "pandas",
        "openpyxl",
        "Pillow"  # For logo display
    ]
    
    for package in requirements:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def check_camera():
    """Check camera availability."""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera access successful")
            cap.release()
            return True
        else:
            print("⚠️  Camera not found at index 0, trying other indices...")
            for i in range(1, 4):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    print(f"✅ Camera found at index {i}")
                    cap.release()
                    return True
            print("❌ No camera found")
            return False
    except ImportError:
        print("❌ OpenCV not installed properly")
        return False

def main():
    print("🎯 Face Recognition Attendance System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Check camera
    if not check_camera():
        print("⚠️  Camera test failed, but you can still use the system if you have a camera")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run: python main.py (for GUI)")
    print("2. Run: python cli_test.py (for command line interface)")
    print("3. Run: python test_fixes.py (to test the system)")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during setup: {e}")
        sys.exit(1)
