# main.py
import tkinter as tk
from ui.login_ui import LoginUI

if __name__ == "__main__":
    root = tk.Tk()
    login_ui = LoginUI(root)
    root.mainloop()