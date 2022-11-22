from Tree import Node
from ChildrenND import ChildrenND
from Extent import Calculate
from UCB1_Tuned import Evaluation
import random
from Dictionary import my_dictionary
from tqdm import tqdm
import itertools


class MCTS:
    def __init__(self, data, numberOfIterations, minSupport, mValue):
        self.df = data
        self.numberOfIterations = numberOfIterations
        self.minSupport = minSupport
        self.mValue = mValue
        self.root = self.Root()
        self.dict_obj = my_dictionary()
        self.Already_Expanded_Patterns = []
        self.M = []
        self.P = []

    def Root(self):
        root = []
        for i in range(len(self.df.columns) - 1):
            column = self.df.iloc[:, i].tolist()
            interval = [min(sorted(column)), max(sorted(column))]
            root.append(interval)
        return root

    def TerminalND(self, node):
        obj = Calculate(dataset=self.df, pattern=node.pattern, root=self.root, mValue=None, label=None)
        if obj.extentND()[1] < self.minSupport:
            return True
        else:
            return False

    @staticmethod
    def Best_Child(node):
        evaluation_list = []
        for child in node.children:
            obj = Evaluation(child.reward_list, node.number_of_visits, child.number_of_visits)
            evaluation_list.append(obj.ucbTuned())
        bestC = evaluation_list.index(max(evaluation_list))
        best_Child = node.children[bestC]

        return best_Child

    def Generate_ChildrenND(self, node):
        obj = ChildrenND(dataset=self.df, Pattern=node.pattern, Root=self.root, minimum_support=self.minSupport)
        children = obj.Direct_ChildrenND()
        node.children.clear()
        for child in children:
            node.children.append(Node(child))

    def Generate_ChildrenND_Simulation(self, node):
        obj = ChildrenND(dataset=self.df, Pattern=node.pattern, Root=self.root, minimum_support=self.minSupport)
        children = obj.Direct_ChildrenND_Simulation()
        node.children.clear()
        for child in children:
            node.children.append(Node(child))

    def nodeSelectionND(self, node):
        while not self.TerminalND(node):
            if list(set(node.children) - set(node.already_expanded_children)):
                break
            else:
                # in case the all children are already expanded:
                node = self.Best_Child(node)
                self.Generate_ChildrenND(node)

        return node

    def Expand(self, node):
        notExpanded = list(set(node.children) - set(node.already_expanded_children))
        random_index = random.randint(0, len(notExpanded) - 1)
        New_Expanded_node = notExpanded[random_index]

        if New_Expanded_node.pattern in self.dict_obj.values():
            node.already_expanded_children.append(New_Expanded_node)
            position = list(self.dict_obj.values()).index(New_Expanded_node.pattern)
            New_Expanded_node = list(self.dict_obj.keys())[position]
            New_Expanded_node.parent.append(node)
            node = New_Expanded_node

        else:
            New_Expanded_node.parent.append(node)
            node.already_expanded_children.append(New_Expanded_node)
            self.dict_obj.add(New_Expanded_node, New_Expanded_node.pattern)
            node = New_Expanded_node

        return node

    def RolloutND(self, node, label):
        path = []
        path_of_patterns = []
        reward = 0
        while not self.TerminalND(node):
            self.Generate_ChildrenND_Simulation(node)
            if len(node.children) == 0:
                break
            else:
                random_index = random.randint(0, len(node.children) - 1)

                Selected_Child = node.children[random_index]
                obj = Calculate(dataset=self.df, pattern=Selected_Child.pattern, root=self.root, mValue=self.mValue,
                                label=label)
                path.append(float(obj.mEstimateND()))
                path_of_patterns.append(Selected_Child.pattern)
                reward = max(path)
                node = Selected_Child
        # --------------------------------------------------------------------------------------
        # to implement the top-k-memory strategy where k in our example is 1
        self.M.append(path_of_patterns[path.index(reward)])

        return reward

    @staticmethod
    def Has_parent(node):
        if node.parent is []:
            return False
        else:
            return True

    def Update(self, node, reward):
        node.reward_list.append(reward)
        node.number_of_visits += 1
        Parents_List = []
        if self.Has_parent(node):
            [Parents_List.append(parent) for parent in node.parent]
        if len(Parents_List) > 0:
            for element in Parents_List:
                element.reward_list.append(reward)
                element.number_of_visits += 1
                if self.Has_parent(element):
                    for parent in element.parent:
                        Parents_List.append(parent)

    @staticmethod
    def Union(lst1, lst2):
        final_list = lst1 + lst2
        return final_list

    def best_pattern_ND(self, pool, label):
        lst = []
        for pattern in pool:
            obj = Calculate(dataset=self.df, root=self.root, pattern=pattern, label=label,
                            mValue=self.mValue)
            lst.append(float(obj.mEstimateND()))

        A = [x for _, x in sorted(zip(lst, pool), reverse=True)]
        A = list(k for k, _ in itertools.groupby(A))
        return A[0]

    def monteCarloND(self):
        Labels = list(set(self.df.iloc[:, -1].tolist()))
        rootNode = Node(self.root)
        Pool_Sets = []

        count = 0
        for Label in Labels:
            self.Generate_ChildrenND(rootNode)

            for i in tqdm(range(self.numberOfIterations),
                          desc=f'Class "{Label}": {Labels.index(Label) + 1} Of {len(Labels)}', ascii=False, ncols=75):
                selectedNode = self.nodeSelectionND(rootNode)
                New_Expanded_Node = self.Expand(selectedNode)
                self.Already_Expanded_Patterns.append(New_Expanded_Node.pattern)
                Reward = self.RolloutND(New_Expanded_Node, Label)
                self.Update(New_Expanded_Node, Reward)

            self.P = self.Union(self.Already_Expanded_Patterns, self.M)

            # make sure there are not redundant patterns:
            Without_duplicates = []
            for elem in self.P:
                if elem not in Without_duplicates:
                    Without_duplicates.append(elem)

            # As the task sofar is to only retrieve the pattern that best describes each label:
            print(self.best_pattern_ND(Without_duplicates, Label))

            # reset the configurations for a new iteration:
            self.Already_Expanded_Patterns.clear()
            self.P.clear()
            self.M.clear()
            self.dict_obj.clear()

