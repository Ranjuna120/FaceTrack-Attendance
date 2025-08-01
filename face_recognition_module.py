# Handles face registration and recognition
import face_recognition
import cv2
import os
import numpy as np

class FaceRecognitionModule:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        self.known_face_encodings = []
        self.known_face_names = []
        for file in os.listdir(self.data_dir):
            if file.endswith(".npy"):
                name = file[:-4]
                encoding = np.load(os.path.join(self.data_dir, file))
                # Validate encoding shape
                if encoding.shape == (128,):
                    self.known_face_encodings.append(encoding)
                    self.known_face_names.append(name)
                else:
                    print(f"Warning: Encoding for {name} has invalid shape {encoding.shape}, skipping.")

    def register_face(self, name):
        cap = cv2.VideoCapture(0)
        print("Press 's' to capture face for registration.")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image from camera.")
                break
            cv2.imshow("Register Face", frame)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                rgb_frame = frame[:, :, ::-1]
                face_locations = face_recognition.face_locations(rgb_frame)
                if len(face_locations) == 0:
                    print("No face detected. Try again.")
                elif len(face_locations) > 1:
                    print("Multiple faces detected. Please ensure only one face is visible.")
                else:
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    if face_encodings and face_encodings[0].shape == (128,):
                        np.save(os.path.join(self.data_dir, f"{name}.npy"), face_encodings[0])
                        print(f"Face registered for {name}")
                        break
                    else:
                        print("Face detected but encoding failed or invalid shape. Try again.")
        cap.release()
        cv2.destroyAllWindows()
        self.load_known_faces()

    def recognize_faces(self):
        cap = cv2.VideoCapture(0)
        recognized_names = set()
        print("Press 'q' to stop attendance.")
        while True:
            ret, frame = cap.read()
            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                    recognized_names.add(name)
                cv2.putText(frame, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.imshow("Attendance", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        return list(recognized_names)
