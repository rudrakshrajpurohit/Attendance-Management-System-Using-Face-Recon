# Face Recognition Attendance System

A modern attendance management system using facial recognition technology, featuring a graphical user interface and database integration.

## Features

- Real-time face detection and recognition
- GUI interface for easy interaction
- SQLite database for attendance records
- Check-in and check-out tracking
- Attendance reporting
- Training interface for new faces

## Prerequisites

- Python 3.7+
- OpenCV
- NumPy
- PIL (Python Imaging Library)
- face_recognition
- tkinter (usually comes with Python)
- SQLite3 (usually comes with Python)

## Installation

2. Install required packages:
  bash
  pip install opencv-python
  pip install numpy
  pip install pillow
  pip install face-recognition
  

3. Create required directories:
  mkdir TrainingImage
  mkdir trainer

## Project Structure

face-recognition-attendance/
├── attendance_system.py # Core recognition system
├── database_handler.py # Database operations
├── gui_interface.py # GUI implementation
├── training.py # Face training module
├── main.py # Entry point
├── TrainingImage/ # Directory for training images
├── trainer/ # Directory for trained models
└── attendance.db # SQLite database file

## Usage

1. First, add training images to the `TrainingImage` directory:
   - Name format: `user.ID.SEQUENCE.jpg` (e.g., `user.1.1.jpg`)
   - Multiple images per person recommended

2. Train the system:
   python training.py

3. Run the application:
  python main.py


## GUI Interface

The interface is divided into two main sections:
- Left: Live camera feed with recognition
- Right: Attendance list with refresh option

### Controls
- Start Recognition: Begins face detection
- Stop Recognition: Stops the camera feed
- Refresh Attendance: Updates the attendance list

## Database Structure

### Users Table
- id (PRIMARY KEY)
- name
- role
- created_at

### Attendance Table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- check_in
- check_out

## Code References

Core System:
  python:attendance_system.py
  startLine: 1
  endLine: 70

GUI Implementation:
  python:gui_interface.py
  startLine: 1
  endLine: 113

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenCV team for computer vision tools
- face_recognition library developers
- SQLite team for the database engine

## Troubleshooting

### Common Issues

1. Face Recognition Installation
   - Install CMake first
   - Install Visual Studio Build Tools
   - Try using pre-built wheels if direct installation fails

2. Camera Access
   - Ensure camera permissions are granted
   - Check if another application is using the camera

3. Database Errors
   - Ensure write permissions in application directory
   - Check if SQLite is properly installed

For more issues, please check the Issues section on GitHub.











