# Alternative face recognition implementation with better compatibility
import face_recognition
import cv2
import os
import numpy as np
import config

class FaceRecognitionModuleCompatible:
    def __init__(self, data_dir=None):
        self.data_dir = data_dir or config.DATA_DIR
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

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

    def load_known_faces(self):
        """Load all registered face encodings from .npy files."""
        self.known_face_encodings = []
        self.known_face_names = []
        
        if not os.path.exists(self.data_dir):
            print(f"Data directory {self.data_dir} does not exist. Creating it.")
            os.makedirs(self.data_dir)
            return
        
        npy_files = [f for f in os.listdir(self.data_dir) if f.endswith(".npy")]
        
        if not npy_files:
            print("No registered faces found.")
            return
        
        for file in npy_files:
            name = file[:-4]  # Remove .npy extension
            file_path = os.path.join(self.data_dir, file)
            
            try:
                encoding = np.load(file_path)
                
                # Validate encoding
                if isinstance(encoding, np.ndarray) and encoding.shape == (128,):
                    self.known_face_encodings.append(encoding)
                    self.known_face_names.append(name)
                    print(f"Loaded face encoding for: {name}")
                else:
                    print(f"Warning: Invalid encoding shape for {name}: {encoding.shape}. Deleting file.")
                    os.remove(file_path)
                    
            except Exception as e:
                print(f"Warning: Could not load encoding for {name}: {e}. Deleting corrupted file.")
                try:
                    os.remove(file_path)
                except:
                    pass
        
        print(f"Successfully loaded {len(self.known_face_encodings)} face encodings.")

    def register_face(self, name):
        # Check if name already exists
        if name in self.known_face_names:
            return False, f"Name '{name}' is already registered. Please use a different name."
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            # Try different camera indices
            for i in range(1, 4):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    break
            else:
                return False, "Failed to access camera. Please check if camera is connected and not in use by another application."
        
        # Set camera properties for better quality
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        cv2.namedWindow("Face Registration Preview", cv2.WINDOW_AUTOSIZE)
        captured = False
        frame = None
        
        print(f"Starting face registration for {name}...")
        print("Position your face in the camera and press SPACE to capture, ESC to cancel")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                cap.release()
                cv2.destroyAllWindows()
                return False, "Failed to capture image from camera."
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            preview = frame.copy()
            
            # Draw a rectangle to guide face positioning
            height, width = preview.shape[:2]
            rect_size = min(width, height) // 3
            center_x, center_y = width // 2, height // 2
            x1 = center_x - rect_size // 2
            y1 = center_y - rect_size // 2
            x2 = center_x + rect_size // 2
            y2 = center_y + rect_size // 2
            
            cv2.rectangle(preview, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(preview, "Align face within green box", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(preview, "Press SPACE to capture, ESC to cancel", (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
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
        
        # Process the captured frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Use simple face detection
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        
        if len(face_locations) == 0:
            return False, "No face detected in captured image. Please ensure good lighting and try again."
        elif len(face_locations) > 1:
            return False, "Multiple faces detected. Please ensure only one face is visible and try again."
        
        # Generate face encoding with minimal parameters
        try:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            if face_encodings and len(face_encodings[0]) == 128:
                file_path = os.path.join(self.data_dir, f"{name}.npy")
                np.save(file_path, face_encodings[0])
                self.load_known_faces()
                print(f"Face encoding saved for {name} at {file_path}")
                return True, f"Face registered successfully for {name}"
            else:
                return False, "Face detected but encoding failed. Please try again with better lighting."
        except Exception as e:
            return False, f"Face encoding failed: {str(e)}. Please try again."

    def recognize_faces(self):
        if len(self.known_face_encodings) == 0:
            return []
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            # Try different camera indices
            for i in range(1, 4):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    break
            else:
                raise Exception("Failed to access camera. Please check if camera is connected and not in use by another application.")
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        recognized_names = set()
        frame_count = 0
        recognition_timeout = 300  # frames
        
        print("Starting face recognition for attendance...")
        print("Position yourself in front of the camera. Press 'q' to stop.")
        
        cv2.namedWindow("Attendance Recognition", cv2.WINDOW_AUTOSIZE)
        
        while frame_count < recognition_timeout:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame from camera")
                break
            
            frame_count += 1
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Only process every 5th frame for performance
            if frame_count % 5 == 0:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                try:
                    # Use simpler face detection
                    face_locations = face_recognition.face_locations(rgb_frame, model="hog")
                    
                    if face_locations:
                        # Simple face encoding
                        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                        
                        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                            # Use simple face comparison
                            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
                            name = "Unknown"
                            
                            if True in matches:
                                # Get distances to find best match
                                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                                best_match_index = np.argmin(face_distances)
                                
                                if matches[best_match_index] and face_distances[best_match_index] < 0.6:
                                    name = self.known_face_names[best_match_index]
                                    recognized_names.add(name)
                            
                            # Draw rectangle around face
                            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                            
                            # Draw label
                            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                            font = cv2.FONT_HERSHEY_DUPLEX
                            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
                
                except Exception as e:
                    print(f"Recognition error: {e}")
                    continue
            
            # Show instructions
            cv2.putText(frame, f"Recognized: {', '.join(recognized_names) if recognized_names else 'None'}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'q' to stop", (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Attendance Recognition", frame)
            
            # Check for quit key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"Recognition completed. Found: {list(recognized_names)}")
        return list(recognized_names)
