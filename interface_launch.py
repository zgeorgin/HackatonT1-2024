from tkinter import Tk
from saver_loader import SaverLoader
from gui import GUI

groups = [["dnsd", "sflvhsj", "kjfvj"], ["sljfvn", "kfjv"]]

window = Tk()
#window.state('zoomed')
window.state('normal')
#window.attributes('-fullscreen', True) 
saver_loader = SaverLoader(window)
gui = GUI(window, saver_loader, groups)
saver_loader.gui = gui
window.mainloop()
