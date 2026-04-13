from tkinter import Tk
from gui import Application

def main():
    root = Tk()
    root.title("Alert Management System")
    root.geometry("500x400")
    root.resizable(False, False)
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()