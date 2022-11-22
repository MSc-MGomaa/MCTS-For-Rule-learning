# MCTS For Rule-learning.
How to use the Monte-Carlo Tree Search Algorithm to find the patterns that best describe each class for a given dataset.

## Main Idea
<p align="justify">
In this work, we will use the MCTS algorithm to find the pattern that maximizes a given heuristic (measure) with respect to a class of interest. So, we will consider the pattern mining problem as a game and solve it with the Monte Carlo tree search (MCTS). 

**NOTE**: In the following context, the words Pattern, Rule, Subgroup are used as synonyms.

## MCTS main phases
<p align="center">
<img width="700" height="250" src="https://github.com/MSc-MGomaa/MCTS-For-Rule-learning/blob/da73e33fd4166c525eee8112b3f32283cf7b2289/1_UP.png">
</p>

### (A) Selection phase
<p align="justify">
With a certain number of iterations, the search starts from the root node. In the node selection phase, the goal is to find a node which is not terminal (the node support is greater than the predefined minimum-support value), and contains one or more children that have not yet been expanded to the tree. If all children of the selected node are expanded, the best child is chosen as shown in figure above. Different heuristics can be used to evaluate and return the best child. However, UCB1_tuned equation is adopted in our implementation:

$$ UCB1-Tuned(s, c) = Q(c) + \sqrt{{\ln(N(s)) \over N(c)} \times min \({1 \over 4}, \sigma²(c) + \sqrt{2 \ln(N(s)) \over N(c)} \)} $$

<p align="justify">
Where, Q(c) represents the average of rewards the child node (c) has achieved so far, N(s) is the number of visits the parent node has done so far, N(c) to indicate how often the child node (c) has been visited by the parent node (s), $\sigma²(c)$ the variance of the rewards the child has received so far. It’s important to mention that the UCB1_Tuned is designed mainly to reduce the impact of the exploration term in the original UCB equation by weighting it with either the
factor ${1 \over 4}$ or the variance of rewards obtained by the node so far. Therefore, the node that maximizes the given heuristic is chosen as the best child.
</p>

### (B) Node Expansion
<p align="justify">

Once a node with the preceding conditions is found, one of the children that have not yet been expanded is selected to be expanded. Children that have not yet been expanded are defined as the difference between the list of direct children and the list of children that have already been expanded for the current node. Once found, a child is chosen at random.

### Avoid duplicates within the entire tree
<p align="justify">
In order to avoid duplicates within the entire tree, a dictionary is used. Since every item in the dictionary consists of a key and a value, each key will be used to represent an already expanded node (a node that already exists in the search tree), the value assigned to the key will represent the pattern of the node. Therefore, before adding a new expanded child to the tree, a check is performed to see if the rule represented by the new extended node is already in the dictionary. In case the rule of the new expanded node already exists in the dictionary, a pointer is set from the parent node (of the new expanded node) to the node already in the tree, then the parent node is added to the list of parents for the node already in the tree, then the node already will be returned for the next steps. If the new expanded node does not exist in the dictionary, it will be added to the dictionary as a new key, and returned for the next steps. </p>

### (C) Rollout Phase

<p align="justify">
In contrast to the standard implementation of MCTS, where only leaf nodes are evaluated during the simulation phase, the use of MCTS differs in pattern mining, where any node created during the simulation is taken into account. For that purpose, a new notation called Path has been introduced to specify which nodes in the simulation will be evaluated and how the rewards for these nodes will be accumulated. From the new expanded node, the path is defined as a list of rules starting with S1 and ending with Sn, where n is a direct specialization of n − 1 and is chosen at random. Once the path is built, it remains to calculate the reward to be backpropagated to each parent node until reaching the root node. Each rule in the path is evaluated, and the reward value is calculated as the maximum evaluation value. To evaluate each rule, the M-estimate equation is used:


$$M-Estimate = {p + m \times {p \over P + N} \over p + n + m}$$ 
<p align="justify">
where, m is a hyperparameter value, p and n are the numbers of positive and negative examples covered by the current rule, ${P \over P+N}$ represents the percentage of the positive examples in the current dataset.

### External Memory
<p align="justify">
Moreover, the node with high evaluation value should not be forgotten, as there is no guarantee that this rule will reappear if the specified number of iterations is not enough. Therefore, several memory policies were introduced to preserve the rules with high evaluation values. Several memory policies were introduced such as the top_k_memory policy, where k patterns with highest evaluation values are kept in an external memory structure. In our implementation, the k value is set to one, to save only the rule with the highest evaluation value after each simulation in the external memory.

### (D) Update Phase
<p align="justify">
The goal of this stage is to update the list of rewards and the visits’ number from the new extended node to the root node. Due to the fact that each node may have more than one parent (due to the avoid-duplicates policy we defined above), each parent in the parents’ list will also be updated. So, for each parent, the number of visits is increased by one, and the reward list is updated by appending the reward value of the new expanded node.


## Direct Specializations
<p align="justify">
The phrase "direct children/specializations" was mentioned several times in the previous sections. This section will go into more detail about this process and how to implement it. By thinking of a numerical dataset, where each feature can be represented as an interval/list of values, the rule can be defined as a list of intervals, where the number of intervals is equal to the number of features.

<p align="justify">
The process of creating direct specializations starts with finding the unique values of each feature in the given dataset, then sorts the values in such a way that each feature can be represented as $feature(i) = [min, ........,max]$, the results are added to the columns list. Under the assumption that, the dataset consists of $n$ features, the columns list can be represented as columns = ${feature(1), feature(2)........, feature(n)}$. Each rule can be represented as a list of intervals, where $rule(i) = [[a1, b1], ........, [an, bn]]$, where $ai, bi ∈ feature(i)$.

<p align="justify">
Finding the index of each $a_i$ and $b_i$ in the list of unique values which represents $feature(i)$ is the core idea of this process. If the difference between the indices $a_i$ and $b_i$ is less than one, then the two values are adjacent in the list, which means that this interval cannot be used to to generate children. While in the case, the difference is greater than one, it means that two children can be delivered from this interval.

<p align="justify">
First, the split_point index is calculated as the average of indices $a_i$ and $b_i$, splitIndex = $index(a_i)$ + $index(b_i)/2$. Suppose the resulting value in the list representing the $feature(i)$ is $c_i$, then the two new terms will be $[a_i, c_i]$ and $[c_i, b_i]$. The two new intervals will replace $[ai, bi]$ in the rule keeping all other intervals unchanged, to produce two children of the current interval, then the process is repeated for all other features in the rule.



### An Illustrative example

<p align="justify">
The process of creating direct specializations depends primarily on the length of the list of unique values for each feature in the dataset. Under the assumption that, the current dataset is a uni-variate type, consists of only one feature, and that feature can be summarized as a list of sex unique values as shown in the figure below, then the intervals that can be generated from that list can be calculated from the equation (2 × n − 3), where n represents the length of the list of unique
values. Applying this to the previous example, we find that (2 × 6 − 3) = 9, which can be listed as follow, [1, 6], [1, 3], [3, 6], [1, 2], [2, 3], [3, 4],
<p align="justify">
In case of categorical datasets, for a nominal feature a, a symbol v, where v ∈ domain(a) to be added to the body of the rule. In case of a multivariate dataset, the rule′s body may contain conjunctive restrictions, each belong to a specific feature.


<p align="center">
<img width="700" height="350" src="https://github.com/MSc-MGomaa/MCTS-For-Rule-learning/blob/c3091fa6580122a5866f53077f113530718c9d5c/ChildrenGE.png">
</p>

### Avoid duplicates within the same branch
<p align="justify">
In order to avoid duplicates within the same branch of the search tree, two main constraints are set, first, only frequent children are considered, which means that the child needs to meet a predefined minimum-support value, and second, the support of the new generated child must be different from parent rule (covers less samples), as the new child is always more specific than the parent rule.


## An Example for the expected output when using MCTS for Rule-learning
<p align="justify">
In the table below, an example when usising the following configurations, number of iterations = 100, minimum support value = 10, mEstimate value = 10 on the "IRIS" dataset. To read the results, If (SepalLengthCm < 6.9) and (SepalWidthCm < 3.7) and (PetalLengthCm < 1.9) -> (40|0), where this pattern covers 40 samples of the class Iris setosa, and covers no negative samples at all. The same is applied to the other rules for the different classes. 


|               |Configurations |              |              |   Class      |              |
| :---: | :---:  |:---:  |------------- |------------- |------------- |
| Iterations  | Min-support   |M-Estimate |Iris-setosa   |Iris-virginica|Iris-versicolor |
| 100           | 10            |10             | Pattern : (SepalLengthCm < 6.9) and (SepalWidthCm < 3.7) and (PetalLengthCm < 1.9) (40\0) | Pattern: (4.8 < PetalLength) (49\6) |Pattern: (PetalLengthCm < 4.8) and (1.0 < PetalWidthCm) (46\3)|




