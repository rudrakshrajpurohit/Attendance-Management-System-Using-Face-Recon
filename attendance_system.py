import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

class AttendanceSystem:
    def __init__(self):
        self.known_faces = []
        self.known_names = []
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def load_known_faces(self, images_path):
        # Load known faces from a directory
        for filename in os.listdir(images_path):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(images_path, filename)
                image = face_recognition.load_image_file(path)
                encoding = face_recognition.face_encodings(image)[0]
                self.known_faces.append(encoding)
                # Get name from filename (remove extension)
                self.known_names.append(os.path.splitext(filename)[0])
                
    def mark_attendance(self, name):
        with open('attendance.csv', 'a') as f:
            now = datetime.now()
            date_string = now.strftime('%Y-%m-%d')
            time_string = now.strftime('%H:%M:%S')
            f.write(f'{name},{date_string},{time_string}\n')
            
    def start_recognition(self):
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert frame to RGB for face_recognition library
            rgb_frame = frame[:, :, ::-1]
            
            # Find faces in frame
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Check if face matches any known face
                matches = face_recognition.compare_faces(self.known_faces, face_encoding)
                name = "Unknown"
                
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_names[first_match_index]
                    self.mark_attendance(name)
                
                # Draw rectangle around face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                
                # Draw name below face
                cv2.putText(frame, name, (left, bottom + 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            cv2.imshow('Attendance System', frame)
            
            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows() 