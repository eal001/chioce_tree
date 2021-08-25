from tkinter import Frame, Button, filedialog
from tkinter.constants import BOTH, LEFT, YES
from decode import decode
from node import Node
from choice_frame import ChoiceFrame
from constants import BG_COLOR

class LoadBar(Frame):

    def __init__(self, master, filename, content_frame):
        Frame.__init__(self, master, bg=BG_COLOR)
        self.master = master
        self.load_button = Button(self, text="load", highlightbackground=BG_COLOR, command=self.load_file)
        self.filename = filename
        self.root = decode(filename)
        if self.root == None:
            self.root = Node("root", [])

        self.load_button.pack(side=LEFT)
        self.content_frame = content_frame

    
    def load_file(self):
        file_name = filedialog.askopenfilename(initialdir=".", title="Select a File")
        self.filename = file_name
        self.root = decode(file_name)
        self.content_frame = ChoiceFrame(self.master, self.root)
        self.content_frame.pack(fill=BOTH, expand=YES)

