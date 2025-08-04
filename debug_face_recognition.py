import face_recognition
import cv2
import numpy as np

try:
    print("Testing face recognition...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not accessible")
        exit(1)
    
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame")
        cap.release()
        exit(1)
    
    rgb_frame = frame[:, :, ::-1]
    print("Frame captured successfully")
    
    # Test face detection
    face_locations = face_recognition.face_locations(rgb_frame)
    print(f"Face locations found: {len(face_locations)}")
    
    if face_locations:
        # Test face encoding - this is where the error likely occurs
        print("Testing face encodings...")
        encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        print(f"Encodings generated: {len(encodings)}")
        if encodings:
            print(f"First encoding shape: {encodings[0].shape}")
    else:
        print("No faces detected in frame")
    
    cap.release()
    print("Test completed successfully")
    
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
