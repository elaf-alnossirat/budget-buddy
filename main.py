import ttkbootstrap as tb
from ui.login_ui import LoginUI

if __name__ == "__main__":
    root = tb.Window(themename="superhero")  # ✅ important
    LoginUI(root)
    root.mainloop()