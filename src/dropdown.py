from tkinter import OptionMenu, StringVar

class Dropdown(OptionMenu):

    # TODO TO SOLVE THE WHOEL CALLBACK ISSUE, MAYBE HAVE EVEVERY DROPDOWN CONTAIN FRAME, SO THAT ON A HANDLE THE FRAME PROPERTIES CAN BE CHANGED AND REDRAWN?

    def __init__(self, master, choice_nodes, index):
        self.choice_nodes = choice_nodes
        self.chosen = StringVar(master)
        choices = []
        for node in choice_nodes:
            choices.append(node.choice)

        self.chosen.set("---")
        self.index = index
        self.choice_frame = master
        OptionMenu.__init__(self, master, self.chosen, *choices, command=self.handle_change)


    def handle_change(self, event):
        self.index = self.choice_nodes[0].depth
        self.choice_frame.made_selection(self.index, self.get_selected_node(self.chosen.get()))


    def get_selected_node( self, choice ):
        for node in self.choice_nodes:
            if node.choice == choice:
                return node
            
        return None

