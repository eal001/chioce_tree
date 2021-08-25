from tkinter import Frame, Scrollbar, Text
from tkinter.constants import END, NORMAL, RIDGE, RIGHT, WORD, Y
from dropdown import Dropdown


class ChoiceFrame(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.scrollbar = Scrollbar(self, orient="vertical" )
        self.scrollbar.pack(side=RIGHT, fill=Y)
        # current_depth will be defined as the depth of nodes that we are SELECTING at
        self.current_depth = 1
        self.option_menus = []
        self.description_box = None
        self.current_node = None

            
    def initialize_root(self, root):
        self.current_node = root
        choice_nodes = []
        for child in root.children:
            choice_nodes.append(child)

        print("init")
        print(self.current_node)
        self.add_option_menu()
        self.rebuild()

    # this method will add another option menu to the array of menus
    # it will take a selected child from the previous option menu, get
    # its children and offer another choice in a subsequent option menu
    def add_option_menu(self):
        print(self.current_node)
        dropdown = Dropdown(self, self.current_node.children, self.current_depth+1)
        self.option_menus.append(dropdown)


    def add_description_box(self):
        self.description_box = Text(self, wrap=WORD, relief=RIDGE, borderwidth=2, height=7, width=20)
        print("got to a noe with description: " + self.current_node.children[0].choice)
        self.description_box.insert(END, self.current_node.children[0].choice)
        self.description_box.config(state=NORMAL)


    def made_selection(self, index, node):
        self.forget_all()
        self.current_node = node
        self.current_depth = index
        self.option_menus = self.option_menus[0:self.current_depth]
        print(index)
        print(self.option_menus)
        print(self.current_node.choice)
        print(self.current_depth)
        if node.has_description_node:
            self.add_description_box()
        elif len(node.children) > 0:
            self.add_option_menu()
        else: 
            pass
        
        self.rebuild()

    
    def forget_all(self):
        for opt in self.option_menus:
            opt.forget()

        if self.description_box is not None:
            self.description_box.forget()


    def rebuild(self):
        for opt in self.option_menus:
            opt.pack()

        if self.description_box is not None:
            self.description_box.pack()
    
