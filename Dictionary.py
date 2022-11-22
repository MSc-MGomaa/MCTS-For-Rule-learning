# to avoid the duplicities within the whole tree, we will build a dictionary of the so far nodes in the tree,
# dictionary consists of key which will be represented by the full node and a key that will be represented within the
# pattern of that node.

class my_dictionary(dict):
    # __init__ function
    def __init__(self):
        self = dict()

    # Function to add key:value
    def add(self, key, value):
        self[key] = value

