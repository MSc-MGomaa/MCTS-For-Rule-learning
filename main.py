from MCTS import MCTS
import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv('Iris.csv')

    obj = MCTS(data=data, minSupport=10, mValue=10, numberOfIterations=100)
    obj.monteCarloND()
