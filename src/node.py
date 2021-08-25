# Author: Elliot Lee
# Date: 8-6-2021
# Description: This is the file that defines the classes for the nodes in the tree

from tkinter import *
from constants import SELECT_COLOR, FILL_COLOR


# this class will represent the data stored as a choice tree using nodes and children that are also nodes
class Node:

    DIAMETER = 70
    RADIUS = DIAMETER/2
    # An instance of a node in python will have an array of children
    # each edge will represent a choice made for
    def __init__(self, choice, children):
        self.choice = choice
        self.children = children
        self.parent = None
        self.id = 0
        self.depth = 0
        self.memory = None
        self.x0 = 0
        self.y0 = 0
        self.has_description_node = False


    # adds a child to the list, but the child needs to be constructed as a node first    
    def add_child_node(self, new_child):
        new_child.depth = self.depth+1
        new_child.set_parent( self )
        self.children.append(new_child)


    def set_parent(self, parent):
        self.parent = parent

    
    # create a child node with the chioce value, and add to the list
    def add_child_value(self, new_choice):
        child = Node(new_choice, [])
        child.depth = self.depth + 1
        child.set_parent( self )
        self.children.append(child)


    # deletes a child based on index 
    def delete_child_by_index(self, index):
        old_child = self.children.pop(index)
        return old_child
    

    # note: this will only remove the first instance of the to_remove choice
    # additionally, it will not return a value if there is no child with a 
    # choice of the to_return value
    def delete_child_by_value(self, to_remove):
        i = 0
        for child in self.children:
            if child.choice == to_remove:
                old_child = self.children.pop(i)
                return old_child
            i+=1

        return None

    def delete_self(self):
        if(self.parent == None):
            print("cannot delete root")
            return False

        self.parent.has_description_node = False
        for child in self.children:
            child.delete_self()

        self.parent.delete_child_by_value(self.choice)
        return True
    
    # method to be called when the node is clicked on the canvas
    def handle_click(self, canvas):
        print("clicked on node, menu frame will be edited")
        # print("previous selected node: " + self.memory.selected_node.choice)
        # redraws the previously selected node as unselected
        if self.memory.selected_visual != None:
            self.memory.delete_visual(canvas)
            self.memory.delete_text(canvas)
        
        self.memory.selected_node = self
        # print(self.parent)
        # if self.parent != None:
        #     print(self.parent.choice) 
        # print("current selected node: " + self.memory.selected_node.choice)
        canvas_data = self.draw_node(SELECT_COLOR, canvas)
        self.memory.selected_visual = canvas_data[0]
        self.memory.selected_text = canvas_data[1]
        self.memory.increment()

        #for child in self.children:
            #print(child.choice + " ::: " + str(child.id) )


    # method to be called to draw the node onto the canvas
    def draw_node(self, color, canvas):
        # print("drawing node " + self.choice + ", id: " + str(self.id))
        
        # print(self.choice)
        trimmed_choice = self.choice
        if len(self.choice) > 10:
            trimmed_choice = self.choice[0:10]

        tag = self.choice + str(self.id)
        tag = tag.replace(' ',"")
        tag = tag.replace('!',"")
        oval = canvas.create_oval(self.x0, self.y0, self.DIAMETER+self.x0, self.DIAMETER+self.y0, 
            outline=color, fill=FILL_COLOR, width=5, tags=tag)

        text = canvas.create_text(self.x0 + self.RADIUS, self.y0+ self.RADIUS, text=trimmed_choice, tags=tag )
        # print("tag for " + self.choice + " is " + tag)
        # print("binding click to tag")
        canvas.tag_bind(tag, "<Button-1>", lambda event, c=canvas: self.handle_click(c))
        return (oval, text)


    # get path method to be called when you want to know the path taken from the root to the current node
    def get_path(self):
        if(self.parent == None):
            return self.choice

        return self.parent.get_path() + "/" + self.choice

    def get_formatted_path(path):
        return path

