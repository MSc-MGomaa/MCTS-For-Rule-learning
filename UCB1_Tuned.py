import math
import numpy
from statistics import mean


class Evaluation:

    def __init__(self, reward_list, NOV_Parent, NOV_Current):
        self.reward_list = reward_list
        self.NOV_Parent = NOV_Parent
        self.NOV_Current = NOV_Current

    def ucbTuned(self):
        Q = mean(self.reward_list)
        firstTerm = math.log(self.NOV_Parent) / self.NOV_Current

        secondTerm = min(.25, (numpy.var(self.reward_list) +
                               math.sqrt((2 * math.log(self.NOV_Parent)) / self.NOV_Current)))

        result = Q + math.sqrt(firstTerm * secondTerm)

        return result


