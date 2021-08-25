# This class will be used in the storage of what node is selected at any given time
class Memory():

    def __init__(self, node, oval, text):
        self.selected_node = node
        self.selected_visual = oval
        self.selected_text = text
        self.counter = 0

    def delete_visual(self, canvas):
        canvas.delete(self.selected_visual)
        self.selected_visual = None

    def delete_text(self, canvas):
        canvas.delete(self.selected_text)
        self.selected_text = None

    def increment(self):
        self.counter += 1
    
    def decrement(self):
        self.counter -= 1

