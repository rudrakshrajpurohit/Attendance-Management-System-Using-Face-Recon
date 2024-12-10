import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
from attendance_system import AttendanceSystem
from database_handler import DatabaseHandler
from datetime import datetime

class AttendanceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.geometry("1200x700")
        
        self.db = DatabaseHandler()
        self.attendance_system = AttendanceSystem()
        
        self.setup_gui()
        
    def setup_gui(self):
        # Create main frames
        self.left_frame = ttk.Frame(self.root, padding="10")
        self.right_frame = ttk.Frame(self.root, padding="10")
        
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Camera feed
        self.camera_label = ttk.Label(self.left_frame)
        self.camera_label.pack(pady=10)
        
        # Controls
        controls_frame = ttk.Frame(self.left_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(controls_frame, text="Start Recognition", 
                  command=self.start_recognition).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Stop Recognition", 
                  command=self.stop_recognition).pack(side=tk.LEFT, padx=5)
        
        # Attendance List
        ttk.Label(self.right_frame, text="Today's Attendance", 
                 font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        # Treeview for attendance
        self.tree = ttk.Treeview(self.right_frame, columns=('Name', 'Check In', 'Check Out'), 
                                show='headings')
        
        self.tree.heading('Name', text='Name')
        self.tree.heading('Check In', text='Check In')
        self.tree.heading('Check Out', text='Check Out')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Refresh button
        ttk.Button(self.right_frame, text="Refresh Attendance", 
                  command=self.refresh_attendance).pack(pady=10)
        
        self.is_recognition_active = False
        
    def start_recognition(self):
        self.is_recognition_active = True
        self.cap = cv2.VideoCapture(0)
        self.update_camera()
        
    def stop_recognition(self):
        self.is_recognition_active = False
        if hasattr(self, 'cap'):
            self.cap.release()
        
    def update_camera(self):
        if self.is_recognition_active:
            ret, frame = self.cap.read()
            if ret:
                # Process frame for face recognition
                recognized_name = self.attendance_system.process_frame(frame)
                if recognized_name:
                    # Mark attendance in database
                    user_id = self.get_user_id(recognized_name)
                    self.db.mark_attendance(user_id)
                
                # Convert frame for display
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)
            
            self.root.after(10, self.update_camera)
    
    def refresh_attendance(self):
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get today's attendance
        attendance_records = self.db.get_attendance_report()
        
        # Update treeview
        for record in attendance_records:
            name, check_in, check_out = record
            check_in_time = datetime.strptime(check_in, '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
            check_out_time = datetime.strptime(check_out, '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S') if check_out else '-'
            self.tree.insert('', tk.END, values=(name, check_in_time, check_out_time))
    
    def get_user_id(self, name):
        # This is a simplified version. You might want to implement proper user management
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return self.db.add_user(name) 