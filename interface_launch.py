from tkinter import Tk
from saver_loader import SaverLoader
from gui import GUI

groups = [["dnsd", "sflvhsj", "kjfvj"], ["sljfvn", "kfjv"]]

window = Tk()
saver_loader = SaverLoader(window)
gui = GUI(window, saver_loader, groups)
window.mainloop()
