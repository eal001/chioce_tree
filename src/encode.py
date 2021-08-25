# Author: Elliot Lee
# Date: 8-5-2021
# Description: This is the script that stores the tree, from the root already given from the program
from node import Node
from description_node import DescriptionNode
from constants import DELIMITER_1, DELIMITER_2, TYPE_NODE, TYPE_DESC

# encodes a string that uses newlines and formats them to a single line, without new lines
def format(string):
    formatted = string.replace("\n", "`\\n`")
    return formatted


#gets all of the nodes in the structure using a dfs
# returns amount of nodes in the tree 
def node_amt(root):
    count = 0
    stack = []
    stack.append(root)
    current = None

    while(len(stack) != 0):
        current = stack.pop()
        for child in current.children:
            stack.append(child)

        count += 1
    
    return count


# performs a bfs in order to get all the choices
def choices(root):
    choices = []
    queue = []
    queue.insert(0, root)
    current = None

    while(len(queue) != 0):
        current = queue.pop()
        for child in current.children:
            queue.insert(0, child)

        if isinstance(current, DescriptionNode):
            choices.append( format(current.choice) )
        else:
            choices.append(current.choice)
    
    return choices

# performs a bfs through the tree in order to get all the types of the nodes
def types(root):
    types = []
    queue = []
    queue.insert(0, root)
    current = None

    while(len(queue) != 0):
        current = queue.pop()
        for child in current.children:
            queue.insert(0, child)
        
        if isinstance(current, DescriptionNode):
            types.append(TYPE_DESC)
        else: 
            types.append(TYPE_NODE)

    return types


# returns an adj list corresponding to the tree using a bfs
def adj_list(root):
    
    count = 0

    # first assign a unique id / index to each node
    # This segment of code does not have to run if we can guarantee that
    # the nodes already have an existing unique ID
    queue = []
    queue.insert(0, root)
    current = None

    while(len(queue) != 0):
        current = queue.pop()
        for child in current.children:
            queue.insert(0, child)

        current.id = count
        count += 1

    # reset the queue though it should be empty here anyway, and iterate again to get the list 
    list = []
    queue = []
    queue.insert(0, root)
    current = None

    while(len(queue) != 0):
        current = queue.pop()
        temp = []
        for child in current.children:
            queue.insert(0, child)
            temp.append( (child.id) )

        list.append(temp)
        count += 1
    
    return list


# This function will encode the root of the choice tree into 
# text at the specified filename 
def encode(file_name, root):
    # get the number of nodes
    amt = node_amt(root)

    # get the list of all choices in bfs order
    all_choices = choices(root)

    # get the list of all types in bfs order
    all_types = types(root)

    # get the list of connections in bfs order
    connections_list = adj_list(root)

    # open the file and erase contents if they existed before 
    treefile = open(file_name, "w")

    # write the node amt on line 1
    treefile.write(str(amt))
    treefile.write(DELIMITER_1)

    #write the types as comma separated values in line 2
    for type in all_types:
        treefile.write(str(type))
        treefile.write(DELIMITER_2)
    
    treefile.write(DELIMITER_1)

    # write the choices as comma separated values on line 3
    for choice in all_choices:
        treefile.write(str(choice))
        treefile.write(DELIMITER_2)
    
    treefile.write(DELIMITER_1)

    # write the adjacency list as comma separated values, for each line 
    for child_list in connections_list:
        for child in child_list:
            treefile.write(str(child))
            treefile.write(DELIMITER_2)

        treefile.write(DELIMITER_1)


# print("encode")