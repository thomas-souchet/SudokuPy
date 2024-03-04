import customtkinter as ctk
from modules.app import App


# UI config
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


if __name__ == "__main__":
    app = App()
    app.mainloop()
