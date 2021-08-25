
from tkinter import Button, Entry, Text, Frame, Label, Toplevel, Scrollbar
from tkinter.constants import *

from canvas_editor import CanvasEditor
from constants import ERROR_COLOR, LINK_COLOR, ROOT_DELETE_ERROR
from description_node import DescriptionNode


class MenuFrame(Frame, CanvasEditor):

    def __init__(self, master, canvas, root, memory, choice, selected):
        Frame.__init__(self, master)
        CanvasEditor.__init__(self)
        self.add_frame = Frame(self)
        self.node = None
        self.label = Label(self, text=choice, font=("Helvetica", 32))
        self.edit_button = Button(self, text="edit", command=self.edit )
        self.delete_button = Button(self, text="delete", command=self.delete)
        self.add_node_button = Button(self.add_frame, text="add node", command=self.add_node)
        self.add_desc_button = Button(self.add_frame, text="add description", command=self.add_desc)
        
        # for reillustrating the graph
        self.canvas = canvas
        self.root = root
        self.memory = memory

        if( not selected): 
            self.edit_button["state"] = DISABLED
            self.delete_button["state"] = DISABLED
            self.add_node_button["state"] = DISABLED
            self.add_desc_button["state"] = DISABLED
        
        self.label.pack(fill=BOTH, expand=YES)
        self.add_node_button.pack(side=LEFT, fill=BOTH, expand=YES)
        self.add_desc_button.pack(side=LEFT, fill=BOTH, expand=YES)
        self.add_frame.pack(fill=BOTH, expand=YES)
        self.edit_button.pack(fill=BOTH, expand=YES)
        self.delete_button.pack(fill=BOTH, expand=YES)
        
    def add_node(self):
        #print("add")
        add_window = Toplevel()
        add_window.geometry("300x80")
        add_window.wm_title("Add a New Choice")
        add_window.resizable(False, False)
        add_window.grab_set()
        label = Label(add_window, text="Choice")
        label.pack(fill=BOTH, expand=YES)
        input = Entry(add_window, text="")
        input.pack( fill=BOTH, expand=YES)
        #print("packing confirm button")
        confirm_button = Button(add_window, text="confirm")
        confirm_button.bind("<Button-1>", lambda event, i=input, w=add_window, o=0: self.add_to_tree(i, w, o) )
        confirm_button.pack()


    def add_desc(self):
        add_window = Toplevel()
        add_window.geometry("300x400")
        add_window.wm_title("Add a New Description")
        add_window.resizable(False, False)
        add_window.grab_set()
        label = Label(add_window, text="Description")
        label.pack(fill=BOTH, expand=YES)
        input = Text(add_window, wrap=WORD, relief=RIDGE, borderwidth=2, height=7, width=20)
        input.pack( fill=BOTH, expand=YES)
        # scrollbar = Scrollbar(text_frame, command=input.yview)
        # scrollbar.pack(side=LEFT)
        # input["yscrollcommand"] = scrollbar.set
        #print("packing confirm button")
        confirm_button = Button(add_window, text="confirm")
        confirm_button.bind("<Button-1>", lambda event, i=input, w=add_window, o=1: self.add_to_tree(i, w, o) )
        confirm_button.pack( fill=BOTH, expand=YES)

            

    def add_to_tree(self, input, window, opt):
        # print("adding")
        # print(input.get())
        if not opt:
            self.node.add_child_value( input.get() )
        else: 
            desc = DescriptionNode( input.get("1.0", "end")) 
            self.node.add_child_node(desc)

        window.destroy()
        self.reset()
        self.illustrate_tree(self.canvas, self.root, self.memory)

    def edit(self):
        # print("edit")
        opt = 0
        edit_window = Toplevel()
        edit_window.geometry("300x80")
        edit_window.wm_title("Edit a Choice")
        edit_window.resizable(False, False)
        edit_window.grab_set()
        label = Label(edit_window, text="Choice")
        label.pack(fill=BOTH, expand=YES)
        # print(self.node.choice)
        input = Entry(edit_window, text="")
        #case for a description node
        if( isinstance(self.memory.selected_node, DescriptionNode)):
            edit_window.geometry("300x400")
            input = Text(edit_window, wrap=WORD, relief=RIDGE, borderwidth=2, height=7, width=20)
            opt = 1
            
        input.insert(END, self.node.choice)
        input.pack(fill=BOTH, expand=YES)
        confirm_button = Button(edit_window, text="confirm")
        confirm_button.bind("<Button-1>", lambda event, i=input, w=edit_window, o=opt: self.edit_tree(i, w, o) )
        confirm_button.pack()

    def edit_tree(self, input, window, opt):
        # print("editing")
        if opt == 1:
            self.node.choice = input.get("1.0", END)
        else: 
            self.node.choice = input.get()

        window.destroy()
        self.reset()
        self.illustrate_tree(self.canvas, self.root, self.memory)

    def delete(self):
        # print("delete")
        delete_window = Toplevel()
        delete_window.geometry("300x100")
        delete_window.wm_title("Delete Choice")
        delete_window.resizable(False, False)
        delete_window.grab_set()
        label = Label(delete_window, text="Delete \'" + str(self.node.choice) + "\' and all of its children?")
        if( isinstance(self.memory.selected_node, DescriptionNode)):
            label.config(text= "Delete \'" + str(self.node.get_formatted_path()) + "\' ?")

        label.pack(fill=BOTH, expand=YES)
        confirm_button = Button(delete_window, text="yes") 
        confirm_button.bind("<Button-1>", lambda event, w=delete_window: self.delete_from_tree(w))
        confirm_button.pack()
        reject_button = Button(delete_window, text="no")
        reject_button.bind("<Button-1>", lambda event, w=delete_window: self.dont_delete_from_tree(w) )
        reject_button.pack()


    def delete_from_tree(self, window):
        # print("deleting")
        success = self.node.delete_self()
        window.destroy()
        if( not success ):
            alert_box = Toplevel()
            alert_box.geometry("300x100")
            alert_box.wm_title("Delete Choice")
            alert_box.resizable(False, False)
            alert_box.grab_set()
            label = Label(alert_box, text=ROOT_DELETE_ERROR, fg=ERROR_COLOR)
            label.pack(fill=BOTH, expand=YES)
            button = Button(alert_box, text="cancel", command=alert_box.destroy)
            button.pack()
        else :
            self.reset()
            self.illustrate_tree(self.canvas, self.root, self.memory)

        
    def reset(self):
        self.memory.selected_node = None
        self.memory.delete_visual(self.canvas)
        self.memory.delete_text(self.canvas)
        self.label.config(text="No Choice Selected") 
        self.edit_button["state"] = DISABLED
        self.delete_button["state"] = DISABLED
        self.add_node_button["state"] = DISABLED
        self.add_desc_button["state"] = DISABLED


    def dont_delete_from_tree(self, window):
        print("not deleting")
        window.destroy()

