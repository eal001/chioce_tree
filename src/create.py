# Author: Elliot Lee
# Date 8-7-2021
# Description:  This is the application that will be used to build / modify the tree
# Resources: http://llimllib.github.io/pymag-trees/
#            https://cs.brown.edu/people/rtamassi/gdhandbook/chapters/trees.pdf

from tkinter import *

from node import Node
from description_node import DescriptionNode
from memory import Memory
from menu import MenuFrame
from toolbar import Toolbar
import decode
from constants import FILE_NAME, BG_COLOR, TITLE, DELIMITER_3, DELIMITER_1


# function to handle clicking the canvas in general
def handle_click(mem, canvas):
    mem.decrement()

    if mem.counter < 0:
        mem.counter = 0
        mem.selected_node = None
        mem.delete_visual(canvas)
        mem.delete_text(canvas)
        menu_frame.label.config(text="No Choice Selected") 
        menu_frame.edit_button["state"] = DISABLED
        menu_frame.delete_button["state"] = DISABLED
        menu_frame.add_node_button["state"] = DISABLED
        menu_frame.add_desc_button["state"] = DISABLED
    else:
        if isinstance(mem.selected_node, DescriptionNode):
            formatted_text = mem.selected_node.get_formatted_path()
            menu_frame.label.config(text=formatted_text)
            menu_frame.edit_button["state"] = NORMAL
            menu_frame.delete_button["state"] = NORMAL
            menu_frame.add_node_button["state"] = DISABLED
            menu_frame.add_desc_button["state"] = DISABLED 
        elif mem.selected_node.has_description_node:
            menu_frame.label.config(text=mem.selected_node.choice)
            menu_frame.edit_button["state"] = NORMAL
            menu_frame.delete_button["state"] = NORMAL
            menu_frame.add_node_button["state"] = DISABLED
            menu_frame.add_desc_button["state"] = DISABLED
        elif len(mem.selected_node.children) > 0:
            menu_frame.label.config(text=mem.selected_node.choice)
            menu_frame.edit_button["state"] = NORMAL
            menu_frame.delete_button["state"] = NORMAL
            menu_frame.add_node_button["state"] = NORMAL
            menu_frame.add_desc_button["state"] = DISABLED
        else:
            menu_frame.label.config(text=mem.selected_node.choice)
            menu_frame.edit_button["state"] = NORMAL
            menu_frame.delete_button["state"] = NORMAL
            menu_frame.add_node_button["state"] = NORMAL
            menu_frame.add_desc_button["state"] = NORMAL 

        

    menu_frame.node = mem.selected_node


# script begins here
window = Tk()
window.geometry("1600x800")
mem = Memory(None, None, None)
root = decode.decode(FILE_NAME)
if root == None:
    root = Node("root", [])
# print(font.families())
# dummy data #
# blueberry = Node("blueberry", [], window)
# raspberry = Node("raspberry", [], window)
# cheese = Node("cheese", [], window)
# apple = Node("apple", [], window)
# strawberry = Node("strawberry", [], window)
# red = Node("red", [apple, strawberry], window)
# blue = Node("blue", [blueberry, raspberry, cheese], window)
# green = Node("green", [], window)
# yellow  = Node("yellow", [], window)
# right = Node("right", [blue], window)
# middle = Node("middle", [green, yellow], window)
# left = Node("left", [red], window)
# root = Node("root", [left, middle, right], window)

content = PanedWindow(window, borderwidth=10, sashwidth=15, handlepad=0, bg="gray")

canvas1 = Canvas(content, bd=0, bg=BG_COLOR)
default_menu = MenuFrame(content, canvas1, root, mem, "No Choice Selected", selected=FALSE)
menu_frame = default_menu
toolbar = Toolbar(window, menu_frame, canvas1, root, mem, FILE_NAME)

toolbar.pack(fill=BOTH, side=TOP)
content.pack(fill=BOTH, expand=YES)
menu_frame.pack(fill=BOTH, expand=YES)
content.add(menu_frame, stretch="always")

canvas1.bind("<Button-1>", lambda event, memory = mem, c = canvas1: handle_click(memory, c) )
menu_frame.illustrate_tree(canvas1, root, mem )
content.add(canvas1, stretch="always")

window.title(TITLE)
window.attributes("-topmost", True)
window.lift()
window.focus_force()
window.grab_set()
window.grab_release()
window.mainloop()

