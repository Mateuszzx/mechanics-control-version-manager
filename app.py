from customtkinter import CTk
from src.gui.main_window import MainWindow

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("3D File Version Tracker")
        self.geometry("1000x600")
        self.main_window = MainWindow(self)
        self.main_window.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()