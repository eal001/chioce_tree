from tkinter import Canvas
from constants import DELIMITER_1, DELIMITER_3, FILL_COLOR
from node import Node
# This class will act as a node, but will be ilustrated differently on the canvas
# additionally when traversing, and a description node is reached, traversal should stop
# it is the final description and categorization of the choices made up to this point
# technically it can have children but it never should
class DescriptionNode(Node):

    def __init__(self, choice):
        Node.__init__(self, choice, [])


    def get_path(self):
        if( self.parent == None ):
            return self.parent.choice
        
        return self.parent.choice + "/" + self.get_path(self.parent)


    def draw_node(self, color, canvas):
        #TODO: fix issues here basically
        trimmed_choice = self.choice
        trimmed_choice = trimmed_choice.replace('\n', "")
        display_choice = ""

        counter = 0
        limit = 36 if 36 < len(trimmed_choice) else len(trimmed_choice)

        for i in range(0, limit):
            if(counter == 9):
                counter = 0
                display_choice += DELIMITER_1
                display_choice += trimmed_choice[i]
            else:
                display_choice += trimmed_choice[i]
            
            counter += 1
        
        tag = self.choice + str(self.id)
        print("pretag")
        print(tag)
        tag = tag.replace(' ',"")
        tag = tag.replace('\n',"")
        tag = tag.replace('!',"")
        print(tag)

        oval = canvas.create_rectangle(self.x0, self.y0, self.DIAMETER+self.x0, self.DIAMETER+self.y0, 
            outline=color, fill=FILL_COLOR, width=5, tags=tag)

        text = canvas.create_text(self.x0 + self.RADIUS, self.y0+ self.RADIUS, text=display_choice, tags=tag )
        canvas.tag_bind(tag, "<Button-1>", lambda event, c=canvas: self.handle_click(c))
        return (oval, text)


    def get_path(self):
        return self.parent.get_path() + "/description"

    
    def get_formatted_path(self):
        path = self.get_path()
        list = self.path_to_list(path)
        formatted = self.format_list(list)
        return formatted

    def path_to_list(self, str):
        start = 0
        end = 0
        list = []
        for char in str:
            if char == DELIMITER_3:
                list.append(str[start:end])
                start = end + 1

            end += 1

        list.append(str[start:end])
        return list


    def format_list(self, list):
        formatted = ""
        counter = 0
        for item in list:
            if(counter == 3):
                counter = 0
                formatted += DELIMITER_1
            
            formatted += DELIMITER_3 + item 
            counter +=1

        return formatted

    def set_parent( self, parent):
        parent.has_description_node = True
        self.parent = parent

