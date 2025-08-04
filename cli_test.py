#!/usr/bin/env python3
"""
Command line test for face recognition system
"""

from face_recognition_module import FaceRecognitionModule
from attendance_manager import AttendanceManager
import sys

def main():
    print("=== Face Recognition Test ===")
    
    face_module = FaceRecognitionModule()
    attendance_manager = AttendanceManager()
    
    while True:
        print("\nOptions:")
        print("1. Register a new face")
        print("2. Start attendance recognition")
        print("3. Show registered faces")
        print("4. Mark manual attendance")
        print("5. Export attendance to Excel")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            name = input("Enter name for registration: ").strip()
            if name:
                print(f"\nRegistering face for: {name}")
                print("Camera will open. Position your face and press SPACE to capture, ESC to cancel.")
                success, message = face_module.register_face(name)
                print(f"Result: {message}")
            else:
                print("Please enter a valid name.")
        
        elif choice == "2":
            print("\nStarting face recognition for attendance...")
            print("Camera will open. Position yourself in front of camera. Press 'q' to stop.")
            try:
                recognized = face_module.recognize_faces()
                if recognized:
                    print(f"\nRecognized faces: {', '.join(recognized)}")
                    for name in recognized:
                        attendance_manager.mark_attendance(name)
                    print("Attendance marked successfully!")
                else:
                    print("No faces recognized.")
            except Exception as e:
                print(f"Error during recognition: {e}")
        
        elif choice == "3":
            registered = face_module.get_registered_names()
            if registered:
                print(f"\nRegistered faces: {', '.join(registered)}")
            else:
                print("\nNo faces registered yet.")
        
        elif choice == "4":
            name = input("Enter name for manual attendance: ").strip()
            if name:
                attendance_manager.mark_attendance(name)
                print(f"Manual attendance marked for: {name}")
            else:
                print("Please enter a valid name.")
        
        elif choice == "5":
            try:
                attendance_manager.export_to_excel()
                print("Attendance exported to Excel successfully!")
            except Exception as e:
                print(f"Export failed: {e}")
        
        elif choice == "6":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
