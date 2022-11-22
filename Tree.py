class Node:

    def __init__(self, pattern):
        self.pattern = pattern
        self.number_of_visits = 0
        self.reward_list = []
        self.children = []
        self.parent = []
        self.already_expanded_children = []
