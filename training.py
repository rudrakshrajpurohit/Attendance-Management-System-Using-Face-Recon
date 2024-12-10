import cv2
import os
import numpy as np
from PIL import Image

# Initialize face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def getImagesAndLabels(path):
    # Get paths of all files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        # Load image and convert to grayscale
        pilImage = Image.open(imagePath).convert('L')
        
        # Convert PIL image to numpy array
        imageNp = np.array(pilImage, 'uint8')
        
        # Get the ID from the image filename
        # Assuming filename format: user.1.jpg, user.2.jpg, etc.
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        
        # Detect faces in the image
        faces = detector.detectMultiScale(imageNp)
        
        # If face is detected, append to samples
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y+h, x:x+w])
            ids.append(id)
            
    return faceSamples, ids

def train_model():
    print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    
    # Path to the folder containing training images
    faces, ids = getImagesAndLabels('TrainingImage')
    
    # Train the model
    recognizer.train(faces, np.array(ids))
    
    # Save the model
    recognizer.write('trainer/trainer.yml')
    
    print(f"\n [INFO] {len(np.unique(ids))} faces trained. Exiting Program")

if __name__ == "__main__":
    # Create trainer directory if it doesn't exist
    if not os.path.exists('trainer'):
        os.makedirs('trainer')
    
    train_model() 