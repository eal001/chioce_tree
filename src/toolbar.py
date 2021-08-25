from tkinter import Button, Frame
from tkinter.constants import *
from constants import BG_COLOR
from encode import encode
from decode import decode
from canvas_editor import CanvasEditor
from tkinter import filedialog


class Toolbar(Frame, CanvasEditor):

    def __init__(self, master, menu, canvas, root, memory, filename):
        Frame.__init__(self, master, background=BG_COLOR, padx=10)
        file_button = Button(self, text="load", highlightbackground=BG_COLOR, command=self.load_file )
        file_button.pack(side=LEFT)
        save_button = Button(self, text="save", highlightbackground=BG_COLOR, command=self.save)
        save_button.pack(side=LEFT)
        saveto_button = Button(self, text="save to", highlightbackground=BG_COLOR, command=self.save_to)
        saveto_button.pack(side=LEFT)
        self.filename = filename
        self.canvas = canvas
        self.root = root
        self.memory = memory
        self.menu = menu

    def save(self):
        # print("saving")
        # print(self.root)
        encode(self.filename, self.root)

    def save_to(self):
        # print("saving to directory")
        file_name = filedialog.asksaveasfilename(title="Choose a Location to Save")
        # print(file_name)
        self.filename = file_name
        encode(self.filename, self.root)

    def load_file(self):
        # print("load file")
        file_name = filedialog.askopenfilename(initialdir=".", title="Select a File")
        self.filename = file_name
        self.root = decode(file_name)
        self.illustrate_tree(self.canvas, self.root, self.memory)
        self.menu.root = self.root
        self.menu.memory = self.memory

   