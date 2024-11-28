from tkinter import Tk
from saver_loader import SaverLoader
from gui import GUI

groups = [["dnsd", "sflvhsj", "kjfvj"], ["sljfvn", "kfjv"]]

window = Tk()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

saver_loader = SaverLoader(window)
gui = GUI(window, saver_loader, groups)
saver_loader.gui = gui
window.geometry(f"{screen_width - 10}x{screen_height - 10}+0+0")
window.mainloop()
