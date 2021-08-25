# Author: Elliot Lee
# Date: 8-6-2021
# Description: This is the script that builds the tree, from the compressed / stored data
from node import Node
import encode
from description_node import DescriptionNode
from constants import DELIMITER_2, TYPE_DESC

def format(string):
    in_graves = False
    format_part = ""
    formatted = ""
    for c in string:
        if c == "`":
            in_graves = not in_graves
            formatted += format_part.replace("\\n", "\n")
            format_part = ""
            
        elif in_graves:
            format_part += c
        else: 
            formatted += c

    return formatted
            


# takes the choices array that was read from line 2 of the treefile and
# turns them into an array of choices bfs order
def decode_choices(choice_str):
    start = 0
    end = 0
    choice_list = []
    for char in choice_str:
        if char == DELIMITER_2:
            choice_list.append(format(choice_str[start:end]))
            start = end + 1

        end += 1

    return choice_list


#takes the string of csv of types that was read from the treefile and turns them into an array
# This should be interpreted from bfs order -- Depends on the encoding method
def decode_types(type_str):
    start = 0
    end = 0
    type_list = []
    for char in type_str:
        if char == DELIMITER_2:
            # print(str(type_str[start:end]) + " s: " + str(start) + " e: " + str(end))
            type_list.append(type_str[start:end])
            start = end + 1

        end += 1

    return type_list


# takes the list of strings that have been read from the treefile and 
# turns them in to edge relationships
def decode_list(list_lines):
    list = []
    sub_list = []
    start = 0
    end = 0
    for line in list_lines:
        sub_list = []
        start = 0
        end = 0
        for char in line:
            if char == DELIMITER_2:
                sub_list.append(int(line[start:end]))
                start = end + 1

            end += 1
        
        list.append(sub_list)
    
    return list


# recurses through all possible children of the tree, and rebuilds based on the id
def reconstruct(adj_list, choices, types, root):
    # print("reconstructing node " + root.choice )
    for child_id in adj_list[root.id]:
        temp = Node(choices[child_id], [])
        if types[child_id] == TYPE_DESC:
            temp = DescriptionNode(choices[child_id])
        temp.id = child_id
        temp.parent = root
        root.add_child_node(temp)
        reconstruct(adj_list, choices, types, temp)
    
    return root


# this function will take the root, and iterate dfs wise in order to assign the correct
# depth to each node
def apply_depth(root):
    stack = []
    stack.append(root)
    current = None
    root.depth = 0

    while(len(stack) != 0):
        current = stack.pop()
        for child in current.children:
            child.depth = current.depth + 1
            stack.append(child)
    

# decodes the text storage of the tree and
def decode(file_name):
    try:
        treefile = open(file_name, "r")

        # get the amount of nodes in the tree
        amt_str = treefile.readline()
        amt = int(amt_str)

        #get the types for each node
        type_str = treefile.readline()
        types = decode_types(type_str)
        # print(type_str)
        # print(types)

        # get the choices for each node
        choice_str = treefile.readline()
        choices = decode_choices(choice_str)

        # get the adj list for each node
        list = []
        for i in range(0, amt):
            list.append( treefile.readline() )

        adj_list = decode_list(list)

        # reconstruct a tree
        root = Node(choices[0], [])
        root.id = 0
        reconstruct(adj_list, choices, types, root)
        apply_depth(root)

        return root
    except IOError:
        return None
        
