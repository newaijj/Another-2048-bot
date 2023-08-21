from config import *

class Node:
    def __init__(self,state,depth,actions=[],toggleChanceNode=False,parent=None):
        self.state = state
        self.depth = depth
        self.actions = actions
        self.isChanceNode = toggleChanceNode

        # used for back propogating evaluation
        self.parent = parent
        self.childrenValues = []
        self.value = None
        self.numChildren = 0
    
    def applyAction(self,action): # -> Node
        assert(not self.isChanceNode)
        newState = self.state.apply(action)
        newActions = self.actions + [action]
        return Node(newState,self.depth+1,newActions,toggleChanceNode=True,parent=self)
    
    def applyRandom(self): # -> Node
        assert(self.isChanceNode)
        newState, twoPos = self.state.addTwo()
        newActions = self.actions + [twoPos]
        return Node(newState,self.depth,newActions,toggleChanceNode=False,parent=self)
    
    # Called on lowest level chance nodes (lowest level chance nodes not expanded)
    def evaluate(self,noChildFlag=False):
        if(noChildFlag):
            self.value = -1e9
        else:
            self.value = self.state.evaluate()
        if(self.parent!=None):
            self.parent.returnChildValue(self.value)

    # Called by children to return their value
    def returnChildValue(self,val):
        self.childrenValues += [val]
        # If all children have returned their values, calculate own value
        if(len(self.childrenValues)==self.numChildren):
            if(self.isChanceNode):
                self.value = sum(self.childrenValues)/len(self.childrenValues)
            elif(not self.isChanceNode):
                self.value = max(self.childrenValues)

            # If we have a parent, pass our value
            if(self.parent!=None) :
                self.parent.returnChildValue(self.value)
