from Extent import Calculate
import pandas as pd


class ChildrenND:
    def __init__(self, dataset, Root, Pattern, minimum_support):
        self.df = dataset
        self.Root = Root
        self.Pattern = Pattern
        self.constant = pd.DataFrame(Pattern)
        self.minimum_support = minimum_support

    # 1: Direct children, to build the tree:
    def Direct_ChildrenND(self):
        # Returns:
        Direct_Children = []

        # First we will represent each feature as a list:
        Columns = []
        df = self.df.iloc[:, :-1]
        for col in df:
            column = df[col].unique().tolist()
            Columns.append(sorted(column))

        obj = Calculate(dataset=df, pattern=self.Pattern, root=self.Root, mValue=None, label=None)
        Extent_of_parent = obj.extentND()[1]

        # If the current Pattern is the Root pattern:
        for i in range(len(self.Pattern)):
            self.Pattern = self.constant.values.tolist()
            Current_Column = Columns[i]
            Current_Interval = self.Pattern[i]
            Left = Current_Column.index(Current_Interval[0])
            Right = Current_Column.index(Current_Interval[1])

            if Right - Left > 1:
                Split_index = int((Left + Right) / 2)
                Child1 = [Current_Column[Left], Current_Column[Split_index]]
                Child2 = [Current_Column[Split_index], Current_Column[Right]]
                # compose the full child pattern:
                self.Pattern[i] = Child1
                # 1: pattern is frequent:
                obj = Calculate(dataset=df, pattern=self.Pattern, root=self.Root, mValue=None, label=None)
                if obj.extentND()[1] >= self.minimum_support:
                    # 2: the child has different support from the parent:
                    if obj.extentND()[1] != Extent_of_parent:
                        Direct_Children.append(self.Pattern)
                    else:
                        pass
                else:
                    pass
                self.Pattern = self.constant.values.tolist()
                self.Pattern[i] = Child2
                # 1: pattern is frequent:
                obj2 = Calculate(dataset=df, pattern=self.Pattern, root=self.Root, mValue=None, label=None)
                if obj2.extentND()[1] >= self.minimum_support:
                    # 2: the child has different support from the parent:
                    if obj2.extentND()[1] != Extent_of_parent:
                        Direct_Children.append(self.Pattern)
                    else:
                        pass
                else:
                    pass
            else:
                pass

        return Direct_Children

    # Allow the generation of the non-frequent patterns, to stop the simulation.
    def Direct_ChildrenND_Simulation(self):
        Direct_Children = []
        Columns = []
        df = self.df.iloc[:, :-1]
        for col in df:
            column = df[col].unique().tolist()
            Columns.append(sorted(column))

        obj = Calculate(dataset=df, pattern=self.Pattern, root=self.Root, mValue=None, label=None)
        Extent_of_parent = obj.extentND()[1]

        for i in range(len(self.Pattern)):
            self.Pattern = self.constant.values.tolist()
            Current_Column = Columns[i]
            Current_Interval = self.Pattern[i]
            Left = Current_Column.index(Current_Interval[0])
            Right = Current_Column.index(Current_Interval[1])

            if Right - Left > 1:
                Split_index = int((Left + Right) / 2)
                Child1 = [Current_Column[Left], Current_Column[Split_index]]
                Child2 = [Current_Column[Split_index], Current_Column[Right]]
                self.Pattern[i] = Child1
                # the child has different support from the parent:
                obj = Calculate(dataset=df, pattern=self.Pattern, root=self.Root, mValue=None, label=None)
                if obj.extentND()[1] != Extent_of_parent:
                    Direct_Children.append(self.Pattern)
                else:
                    pass
                self.Pattern = self.constant.values.tolist()
                self.Pattern[i] = Child2
                obj2 = Calculate(dataset=df, pattern=self.Pattern, root=self.Root, mValue=None, label=None)
                if obj2.extentND()[1] != Extent_of_parent:
                    Direct_Children.append(self.Pattern)
                else:
                    pass
            else:
                pass

        return Direct_Children
