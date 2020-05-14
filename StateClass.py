##-------------------------------LIBRARIES----------------------------------##

from GridFunctions import State2Grid
import operator
from random import random

##-----------------------------Class definition-----------------------------##
"""
The objects of type State will have the following attributes:
    -int number      : It is the first identifier of the state
    -int vPos        : It is the row in which the state is placed (from 0 to H-1)
    -int hPos        : It is the column in which the state is placed (from 0 to W-1)
    -boolean initial : True if this is the initial state
    -boolean goal    : True if this is the goal
    -boolean obstacle: True if this state is a dead-end, otherwise False
    -boolean top     : True if the state belongs to the top bound, otherwise False
    -boolean bottom  : True if the state belongs to the bottom bound, otherwise False
    -boolean rigth   : True if the state belongs to the right bound, otherwise False
    -boolean left    : True if the state belongs to the left bound, otherwise False
    -dictionary transitions : This is an attribute that must be defined by a 
                              declarative model generator. The recommended data
                              structure can be as follows:
                              transitions = {"action" : {State prime : [Probability,Cost]}}
    -float value: current estimate for the value of this state
"""
class State:
    
    def __init__(self, index, H, W):
        
        # Positon attributes
        self.number = index
        [self.vPos,self.hPos] = State2Grid(index, H, W)
         
        # Special States
        self.initial = False
        self.goal = False
        self.obstacle = False
        
        # Border detection
        if self.vPos == 0:
            self.top = True
        else:
            self.top = False
            
        if self.vPos == H-1:
            self.bottom = True
        else:
            self.bottom = False
        
        if self.hPos == 0:
            self.left = True
        else:
            self.left = False
        
        if self.hPos == W-1:
            self.right = True
        else:
            self.right = False
          
        # Transition model    
        self.transitions = {}
        
        #Current estimate of the value function -> (L)RTDP
        self.value = 0
        
        #solved label -> for LRTDP
        self.solved = False
   
         
    def __str__(self):
        return  "s"+str(self.number)+"-(" + str(self.vPos) + "," + str(self.hPos) + ")"
    
    
    ## useful methods for RTDP -----------------------------------------------    
    def Qvalue(self, action, gamma):
        
        """
        This method computes the Q value for a pair state-action, taking into
        account the current estimate for the values of the successor's states
        """
        
        Bellman_operator = 0
        for s_prime,parameters in self.transitions[action].items():
            
            Bellman_operator += parameters[0] * (parameters[1] + gamma * s_prime.value)
        
        return Bellman_operator
    
    #-------------------------------------------------------------------------        
    def greedyAction(self, gamma):
        
        """
        This method computes the Q-values for all the possible actions in the 
        given state. According to these results, this method returns the 
        greedy action which maximizes the Q-value
        """
        
        Bellman_dic = {}
        for action in self.transitions.keys():
            
            Bellman_dic[action] = self.Qvalue(action, gamma)
        
        a = max(Bellman_dic.items(), key=operator.itemgetter(1))[0]
        
        return a
    
    #-------------------------------------------------------------------------
    def update(self,gamma):
        
        """
        This method can update the value of a state in accordance with the
        greedy action.
        """
        a = self.greedyAction(gamma)
        self.value = self.Qvalue(a,gamma)
        
    #-------------------------------------------------------------------------
    def sampleNewState(self, action):
        
        """
        This method is able to return an successor state in accoradance with
        the probability P(s'|s,a).
        Obiously, the transition model must be defined before launching this 
        method.
        """
        r = random()           # create a random number in the range [0,1]
        accrualProb = 0        # initialise the accrual Probability
        
        # Explore the dictionary {successor : [Probability, Cost]}
        for s_prime,parameters in self.transitions[action].items():
     
            accrualProb += parameters[0]    # Addup the probability for this successor
            
            if r <= accrualProb:            # if the random number is in this
                                            # range, I can return the successor
                return s_prime
            
            else:
                continue
            
        """
        This is a fair algorithm. Imagine the following example:
            {s1: 0.1,
             s2: 0.8,
             s3: 0.1}
        accrual = 0.1 -> if r<0.1 -> return s1 with a probability of 0.1
        accrual = 0.9 -> if r<0.9 -> return s2 with a probability of 0.8
        accrual = 1.0 -> if r<1.0 -> return s3 with a probability of 0.1
        """
            
    #-------------------------------------------------------------------------       
    def Residual(self, gamma):
        
        """
        This method compares the current value of the state with its possible
        update according to the Q-value with the greedy action.
        """
        
        a = self.greedyAction(gamma)
        
        return abs(self.value - self.Qvalue(a,gamma))
        
    #------------------------------------------------------------------------
     
    def SampleAction(self):
         
        """
        This method returns a random action according to the transitions 
        atribute. this method is used in the rollouts of the UCT algorithm
        """
        r = random()                # sample a random number in the range [0,1]
        nA = len(self.transitions)  # compute the number of actions
        deltaP = 1/nA               # compute an increment of probability
        accrual = 0                 # accrual probability
        for action in self.transitions.keys():
            
            accrual += deltaP       # addup the increment to accrual
            if r <= accrual: return action
            else: continue
                
                