# Basic test for FaceRecognitionModule
from face_recognition_module import FaceRecognitionModule

if __name__ == "__main__":
    frm = FaceRecognitionModule()
    print("Known faces loaded:", frm.known_face_names)
