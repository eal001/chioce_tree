from constants import LINK_COLOR
from encode import node_amt

# this is a utility calss where multiple methods will inherit aspects of
# I am using it to clean up the create file and limit reused code
class CanvasEditor:

    def __init__(self):
        pass


    # this method will loop through each node in the tree and reassign ids to ever node
    # it will use a bfs to remaian consistent with the encoding methods
    def identify(self, root):
        queue = []
        queue.insert(0, root)
        current  = None
        counter = 0
        while (len(queue) != 0):
            current = queue.pop()
            for child in current.children:
                queue.insert(0, child)
            
            current.id = counter
            counter +=1
        

    # bfs through the tree and increment each index at the corresponding depth
    # Will return an array that lists how many nodes exist at each depth  
    def amount_per_depth(self, root):  
        total_nodes = node_amt(root)
        #print("new amt of total nodes")
        #print(total_nodes)
        depth_list = [0]*total_nodes

        queue = []
        queue.insert(0, root)
        current = None
        print(len(queue))

        while (len(queue) != 0) :
            current = queue.pop()
            depth_list[current.depth] += 1
            for child in current.children:
                queue.insert(0, child)

        return depth_list


    # This function will iterate through the choice tree and draw out each node
    def illustrate_tree(self, canvas, root, memory ):
        
        # I dont know where frame will be bound to yet
        canvas.delete("all")
        self.identify(root)
        depth_list = self.amount_per_depth(root)
        marker_list = self.amount_per_depth(root)
        max_val = max(depth_list)
        print(max_val)
        queue = []
        queue.insert(0, root)
        current = None
        
        # bfs through each node and apply properties
        while (len(queue) != 0) :
            current = queue.pop()
            
            # apply memory and (x0, y0) coordinates
            current.memory = memory
            spacing_factor = (max_val*100 / depth_list[current.depth] )
        
            current.x0 = (depth_list[current.depth] - marker_list[current.depth]) * spacing_factor + spacing_factor / 2
            current.y0 = 100*current.depth + 10

            marker_list[current.depth] -= 1
            for child in current.children:
                queue.insert(0, child)

        # bfs through each node and draw the edges
        queue = []
        current = None
        queue.insert(0, root)
        while (len(queue) != 0):
            current = queue.pop()

            for child in current.children:
                queue.insert(0, child)
                # draw lines first
                canvas.create_line(current.x0 + current.RADIUS, current.y0 + current.RADIUS, 
                    child.x0 + child.RADIUS, child.y0 + child.RADIUS, fill=LINK_COLOR, width=5)
            
            # draw circle and bind clicks
            current.draw_node(LINK_COLOR, canvas)
        