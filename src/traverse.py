# Author: Elliot Lee
# Date 8-5-2021
# Description: This is the script that will display a GUI application that traverses a tree of options.

from tkinter import *
from choice_frame import ChoiceFrame 
from loadbar import LoadBar
from constants import FILE_NAME

window = Tk()
content_frame = ChoiceFrame(window)
load_bar = LoadBar(window, FILE_NAME, content_frame)
content_frame.initialize_root(load_bar.root)
content_frame.pack(side=BOTTOM, fill=BOTH, expand=YES)
load_bar.pack(side=TOP, fill=BOTH)

window.title("Traverse")
window.geometry("500x800")
window.attributes("-topmost", True)
window.lift()
window.focus_force()
window.grab_set()
window.grab_release()
window.mainloop()
