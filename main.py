import tkinter as tk
from gui_interface import AttendanceGUI

def main():
    root = tk.Tk()
    app = AttendanceGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 