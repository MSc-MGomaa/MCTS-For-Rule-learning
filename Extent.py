class Calculate:

    def __init__(self, dataset, pattern, root, label, mValue):
        self.df = dataset
        self.pattern = pattern
        self.root = root
        self.label = label
        self.mValue = mValue

    def extentND(self):
        # (self, dataset, root, pattern)
        index = 0
        different_indices = []
        for f, b in zip(self.root, self.pattern):
            if f == b:
                pass
            else:
                different_indices.append(index)
            index += 1

        dataset = self.df.values.tolist()
        Extent_ND = []
        Covered_Labels = []
        index_of_row = 0
        for row in dataset:
            counter = 0
            for x in different_indices:
                if self.pattern[x][0] <= float(row[x]) <= self.pattern[x][1]:
                    counter += 1
                else:
                    break
            if counter == len(different_indices):
                Extent_ND.append(index_of_row)
                Covered_Labels.append(row[-1])
            else:
                pass
            index_of_row += 1

        support = len(Extent_ND)

        return Extent_ND, support, Covered_Labels

    def mEstimateND(self):
        obj = Calculate(dataset=self.df, pattern=self.pattern, root=self.root, label=self.label,
                        mValue=self.mValue)
        support = obj.extentND()[1]
        p = obj.extentND()[2].count(self.label)
        counter2 = self.df.iloc[:, -1].tolist().count(self.label)
        num_samples_within_DS = counter2 / len(self.df)

        M_est = (p + (self.mValue * num_samples_within_DS)) / (support + self.mValue)

        return M_est

    def extentCD(self):
        index = 0
        different_indices = []
        for f, b in zip(self.root, self.pattern):
            if f == b:
                pass
            else:
                different_indices.append(index)
            index += 1

        dataset = self.df.values.tolist()
        Extent_CD = []
        Covered_Labels = []
        index_of_row = 0

        for row in dataset:
            counter = 0
            for x in different_indices:
                if row[x] == 1:
                    counter += 1
                else:
                    break
            if counter == len(different_indices):
                Extent_CD.append(index_of_row)
                Covered_Labels.append(row[-1])
            else:
                pass
            index_of_row += 1

        support = len(Extent_CD)

        return Extent_CD, support, Covered_Labels

    def mEstimateCD(self):
        obj = Calculate(dataset=self.df, pattern=self.pattern, root=self.root, label=self.label, mValue=self.mValue)
        support = obj.extentCD()[1]
        p = obj.extentCD()[2].count(self.label)
        counter2 = self.df.iloc[:, -1].tolist().count(self.label)
        num_samples_within_DS = counter2 / len(self.df)

        M_est = (p + (self.mValue * num_samples_within_DS)) / (support + self.mValue)

        return M_est

    '''
        def __init__(self, dataset, pattern, root, label, mValue):
            self.df = dataset
            self.pattern = pattern
            self.root = root
            self.label = label
            self.mValue = mValue

        def extentND(self):
            # determine the restricted columns:
            columnIndex = 0
            restrictedColumns = []
            for f, b in zip(self.root, self.pattern):
                if f == b:
                    pass
                else:
                    restrictedColumns.append(columnIndex)
                columnIndex += 1

            # loop over all rows:
            coveredLabels = []
            Extent_ND = []

            for ind in self.df.index:
                counter = 0
                for x in restrictedColumns:
                    if self.pattern[x][0] <= self.df.iloc[ind][x] <= self.pattern[x][1]:
                        counter += 1
                    else:
                        break
                if counter == len(restrictedColumns):
                    Extent_ND.append(ind)
                    row = self.df.iloc[ind].tolist()
                    coveredLabels.append(row[-1])

                else:
                    pass

            return Extent_ND, len(Extent_ND), coveredLabels

        def mEstimateND(self):
            obj = CalculateND(dataset=self.df, pattern=self.pattern, root=self.root, label=self.label, mValue=self.mValue)
            support = obj.extentND()[1]
            p = obj.extentND()[2].count(self.label)
            counter2 = self.df.iloc[:, -1].tolist().count(self.label)
            num_samples_within_DS = counter2 / len(self.df)

            M_est = (p + (self.mValue * num_samples_within_DS)) / (support + self.mValue)

            return M_est

        '''
