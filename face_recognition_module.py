# Handles face registration and recognition
import face_recognition
import cv2
import os
import numpy as np

class FaceRecognitionModule:
    def get_registered_names(self):
        """Return a list of registered names (from .npy files in data_dir)."""
        return [file[:-4] for file in os.listdir(self.data_dir) if file.endswith('.npy')]

    def delete_face(self, name):
        """Delete the .npy file for a registered face."""
        file_path = os.path.join(self.data_dir, f"{name}.npy")
        if os.path.exists(file_path):
            os.remove(file_path)
            self.load_known_faces()
            return True
        return False
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
                file_path = os.path.join(self.data_dir, file)
                try:
                    encoding = np.load(file_path)
                    # Validate encoding shape
                    if encoding.shape == (128,):
                        self.known_face_encodings.append(encoding)
                        self.known_face_names.append(name)
                    else:
                        print(f"Warning: Encoding for {name} has invalid shape {encoding.shape}, deleting file.")
                        os.remove(file_path)
                except Exception as e:
                    print(f"Warning: Could not load encoding for {name}: {e}. Deleting file.")
                    os.remove(file_path)

    def register_face(self, name):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False, "Failed to access camera."
        cv2.namedWindow("Face Registration Preview")
        captured = False
        frame = None
        while True:
            ret, frame = cap.read()
            if not ret:
                cap.release()
                cv2.destroyAllWindows()
                return False, "Failed to capture image from camera."
            preview = frame.copy()
            cv2.putText(preview, "Press SPACE to capture, ESC to cancel", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv2.imshow("Face Registration Preview", preview)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                cap.release()
                cv2.destroyAllWindows()
                return False, "Registration cancelled."
            elif key == 32:  # SPACE
                captured = True
                break
        cap.release()
        cv2.destroyAllWindows()
        if not captured or frame is None:
            return False, "No image captured."
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        if len(face_locations) == 0:
            return False, "No face detected. Please try again."
        elif len(face_locations) > 1:
            return False, "Multiple faces detected. Please ensure only one face is visible."
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        if face_encodings and face_encodings[0].shape == (128,):
            np.save(os.path.join(self.data_dir, f"{name}.npy"), face_encodings[0])
            self.load_known_faces()
            return True, f"Face registered for {name}"
        else:
            return False, "Face detected but encoding failed or invalid shape. Try again."

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
