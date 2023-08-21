
from Node import *
from Frontier import *
from State import POSSIBLE_ACTIONS
from config import *

class Search:

    def __init__(self, state):
        self.bfsFrontier = BFSFrontier()
        initialNode = Node(state,0)
        self.bfsFrontier.insert(initialNode)

    # performs the search from the initial state
    # returns the action that gives the best result
    def search(self) -> str:
        bestAction = ""
        bestEvaluation = -1e10

        initialNodes = []

        while self.bfsFrontier.size() > 0:
            node = self.bfsFrontier.next()

            # Pick out depth-1 chance nodes
            if (node.depth == 1 and node.isChanceNode):
                initialNodes.append(node)

            # Check depth limit, trigger evaluation if we have reached LIMIT depth
            if (node.depth == LIMIT and node.isChanceNode):
                node.evaluate()
                continue
                    
            state = node.state
            if(node.isChanceNode):
                node.numChildren = CHANCE_NODE_BRANCHING
                for _ in range(CHANCE_NODE_BRANCHING):
                    newNode = node.applyRandom()
                    self.bfsFrontier.insert(newNode)
            else:
                numChildren = 0
                for action in POSSIBLE_ACTIONS:
                    if state.canMove(action):
                        numChildren += 1
                        newNode = node.applyAction(action)
                        self.bfsFrontier.insert(newNode)
                if(numChildren==0):
                    node.evaluate(noChildFlag=True)
                else:
                    node.numChildren = numChildren

        # Select the best action out of initial action set
        for node in initialNodes:
            print("IF: {}".format(node.actions[0]))
            print("VALUE: {}".format(node.value))
            if(node.value > bestEvaluation):
                bestAction = node.actions[0]
                bestEvaluation = node.value

        assert (bestAction != '')
        return bestAction
