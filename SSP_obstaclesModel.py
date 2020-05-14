"""
This the transition-cost model for the first scenario to test and compare 
several algorithms.

In this planning domain, an automomous agent must travel through a 2D grid-map
avoiding obastacles which have been modeled as dead-ends. That is to say, 
states from which it is impossible to leave thus the agent will never reach 
the goal. The initial state is known and the objective is to find the optimal
(or near-optimal) policy that drives the agent from the inital state to the goal

This benchmark has been modeled as an Stochastic Shortest Path (SSP) in other 
words, a discounted infinite horizon MDP with negative rewards to simulate 
costs. 

"""

##-------------------------------LIBRARIES----------------------------------##

from StateClass import State
from GridFunctions import Grid2State

##------------------------------COST FUNCTION-------------------------------##
"""
This function returns the cost depending on the destination. Three different
costs are defined in this problem:
    -Nominal cost : the regular value for all the actions
    -Goal cost : the cost/reward when tha action takes the agent to the goal
    -obstacle Cost : it is a kind of penalty for crashing against an obstacle
                     and getting traped in a dead-end

This function must be called within the TransCostModel() and it will help to 
complet the transitions dictionary attribute of the State objects

inputs:
    - State state: an initialised state

output:
    - The cost
"""
def Cost(state):
    
    nominalCost = -0.05
    obstacleCost = -5
    goalCost = 0
    
    if state.goal:
        return goalCost
    
    elif state.obstacle:
        return obstacleCost
    
    else:
        return nominalCost



##--------------------TRANSITION-COST-FUNCTION------------------------------##
"""
This function takes an initialised list of states and completes the transitions
dictionary attribute of each State object. Remember from the documentation in
StateClass:
-dictionary transitions : This is an attribute that must be defined by a 
                          declarative model generator. The recommended data
                          structure can be as follows:
        s.transitions = {"action" : {"State prime" : [Probability,Cost]}}

"""
def TransCostModel(states, H, W):
        
    for s in states:
        
        # Stay action definition ---------------------------------------------
        if s.obstacle:
            s.transitions["Stay"] = {s: [1, Cost(s)]}
            
        elif s.goal:
            s.transitions["Stay"] = {s: [1, Cost(s)]}
            
        else:
            s.transitions["Stay"] = {s: [1, Cost(s)]}
            
            
        
        
        # NORTH action definition --------------------------------------------    
        if s.obstacle:
            s.transitions["North"] = {s: [1, Cost(s)]} 
            
        elif s.goal:
            s.transitions["North"] = {s: [1, Cost(s)]}
        
        elif s.top:
            s.transitions["North"] = {s: [1, Cost(s)]}
           
        elif not s.top and s.left :
            #Compute the index of destination states
            d1 = Grid2State(s.vPos-1, s.hPos, H, W)            #Upper state
            d2 = Grid2State(s.vPos-1, s.hPos+1, H, W)          #up-right state
            
            #look for the states in the list
            s1 = states[d1]
            s2 = states[d2]
            
            s.transitions["North"] = {s1: [0.9, Cost(s1)],
                                      s2: [0.1, Cost(s1)]}
            
        elif not s.top and s.right :
            #Compute the index of destination states
            d1 = Grid2State(s.vPos-1, s.hPos, H, W)           #Upper state
            d2 = Grid2State(s.vPos-1, s.hPos-1, H, W)         #up-left state
            
            #look for the states in the list
            s1 = states[d1]
            s2 = states[d2]
            
            s.transitions["North"] = {s1: [0.9, Cost(s1)],
                                      s2: [0.1, Cost(s2)]}
            
        else:
            #Compute the index of destination states
            d1 = Grid2State(s.vPos-1, s.hPos, H, W)            #Upper state
            d2 =  Grid2State(s.vPos-1, s.hPos-1, H, W)         #up-left state
            d3 =  Grid2State(s.vPos-1, s.hPos+1, H, W)         #up-right state
            
            #look for the states in the list
            s1 = states[d1]
            s2 = states[d2]
            s3 = states[d3]
            
            s.transitions["North"] = {s1: [0.8, Cost(s1)],
                                      s2: [0.1, Cost(s2)],
                                      s3: [0.1, Cost(s3)]}
            
        # SOUTH action definition --------------------------------------------
        if s.obstacle:
            s.transitions["South"] = {s: [1, Cost(s)]} 
            
        elif s.goal:
            s.transitions["South"] = {s: [1, Cost(s)]}
        
        elif s.bottom:
            s.transitions["South"] = {s: [1, Cost(s)]}
           
        elif not s.bottom and s.left :
            #Compute the index of destination states
            d1 = Grid2State(s.vPos+1, s.hPos, H, W)            #down state
            d2 = Grid2State(s.vPos+1, s.hPos+1, H, W)          #down-right state
            
            #look for the states in the list
            s1 = states[d1]
            s2 = states[d2]
            
            s.transitions["South"] = {s1: [0.9, Cost(s1)],
                                      s2: [0.1, Cost(s2)]}
            
        elif not s.bottom and s.right :
            #Compute the index of destination states
            d1 = Grid2State(s.vPos+1, s.hPos, H, W)            #down state
            d2 = Grid2State(s.vPos+1, s.hPos-1, H, W)          #down-left state
            
            #look for the states in the list
            s1 = states[d1]
            s2 = states[d2]
            
            s.transitions["South"] = {s1: [0.9, Cost(s1)],
                                      s2: [0.1, Cost(s2)]}
            
        else:
            #Compute the index of destination states
            d1 = Grid2State(s.vPos+1, s.hPos, H, W)            #down state
            d2 = Grid2State(s.vPos+1, s.hPos-1, H, W)          #down-left state
            d3 = Grid2State(s.vPos+1, s.hPos+1, H, W)          #down-right state 
            
            #look for the states in the list
            s1 = states[d1]
            s2 = states[d2]
            s3 = states[d3]
            
            s.transitions["South"] = {s1: [0.8, Cost(s1)],
                                      s2: [0.1, Cost(s2)],
                                      s3: [0.1, Cost(s3)]}
        
        # East action definition ---------------------------------------------
        if s.obstacle:
            s.transitions["East"] = {s: [1, Cost(s)]} 
            
        elif s.goal:
            s.transitions["East"] = {s: [1, Cost(s)]}
        
        elif s.right:
            s.transitions["East"] = {s: [1, Cost(s)]}
           
        elif not s.right and s.top :
            #Compute the index of destination states
            d1 = Grid2State(s.vPos, s.hPos+1, H, W)            #right state
            d2 = Grid2State(s.vPos+1, s.hPos+1, H, W)          #down-right state
            
            #look for the states in the list
            s1 = states[d1]
            s2 = states[d2]
            
            s.transitions["East"] = {s1: [0.9, Cost(s1)],
                                     s2: [0.1, Cost(s2)]}
            
        elif not s.right and s.bottom :
            #Compute the index of destination states
            d1 = Grid2State(s.vPos, s.hPos+1, H, W)            #right state
            d2 = Grid2State(s.vPos-1, s.hPos+1, H, W)          #up-right state
            
            #look for the states in the list
            s1 = states[d1]
            s2 = states[d2]
            
            s.transitions["East"] = {s1: [0.9, Cost(s1)],
                                     s2: [0.1, Cost(s2)]}
            
            
        else:
            #Compute the index of destination states
            d1 = Grid2State(s.vPos, s.hPos+1, H, W)            #right state
            d2 = Grid2State(s.vPos+1, s.hPos+1, H, W)          #down-right state
            d3 = Grid2State(s.vPos-1, s.hPos+1, H, W)          #up-right state 
            
            #look for the states in the list
            s1 = states[d1]
            s2 = states[d2]
            s3 = states[d3]
            
            s.transitions["East"] = {s1: [0.8, Cost(s1)],
                                     s2: [0.1, Cost(s2)],        
                                     s3: [0.1, Cost(s3)]}
            
        # West action definition ---------------------------------------------
        if s.obstacle:
            s.transitions["West"] = {s: [1, Cost(s)]} 
            
        elif s.goal:
            s.transitions["West"] = {s: [1, Cost(s)]}
        
        elif s.left:
            s.transitions["West"] = {s: [1, Cost(s)]}
           
        elif not s.left and s.top :
            #Compute the index of destination states
            d1 = Grid2State(s.vPos, s.hPos-1, H, W)            #left state
            d2 = Grid2State(s.vPos+1, s.hPos-1, H, W)          #down-left state
            
            #look for the states in the list
            s1 = states[d1]
            s2 = states[d2]
            
            s.transitions["West"] = {s1: [0.9, Cost(s1)],
                                     s2: [0.1, Cost(s2)]}
            
        elif not s.left and s.bottom :
            #Compute the index of destination states
            d1 = Grid2State(s.vPos, s.hPos-1, H, W)             #left state
            d2 = Grid2State(s.vPos-1, s.hPos-1, H, W)           #up-left state
            
            #look for the states in the list
            s1 = states[d1]
            s2 = states[d2]
            
            s.transitions["West"] = {s1: [0.9, Cost(s1)],
                                     s2: [0.1, Cost(s2)]}
            
        else:
            #Compute the index of destination states
            d1 = Grid2State(s.vPos, s.hPos-1, H, W)              #left state
            d2 = Grid2State(s.vPos+1, s.hPos-1, H, W)            #down-left state
            d3 = Grid2State(s.vPos-1, s.hPos-1, H, W)            #up-left state 
            
            #look for the states in the list
            s1 = states[d1]
            s2 = states[d2]
            s3 = states[d3]
            
            s.transitions["West"] = {s1: [0.8, Cost(s1)],
                                     s2: [0.1, Cost(s2)],
                                     s3: [0.1, Cost(s3)]}
        
    return states
    

##--------------------DEFINITION OF THE DECLARATIVE MODEL--------------------##
"""
This is the main method of this python code. It initialises the list of states
and calls the functions above to complete the attributes of these states.
The return is a list of states with all the information of the delarative 
model of the problem.

"""
def declarativeModel():
    
    ##------------------DEFINITION OF THE PLANNING DOMAIN-------------------##
    #            -----------------
    #            |S0 |S1 |S2 |S3 |
    #            |S4 |S5 |S6 |S7 |
    #            |S8 |S9 |S10|S11|
    #            -----------------
    
    H = 3                            # Height
    W = 4                            # Width
    n_states = H*W                   # Number of states, including:
                                     #   -Initial, Goal, Obstacles.
    
    
    # Initialization of States
    
    states = []                                
    for i in range (0,n_states):
        states.append(State(i,H,W))
    
    # 1) Initial State
    states[0].initial = True           # S0 will be the initial state
    # 2) Goal State
    states[11].goal = True             # S11 will be the goal
    # 3) Obstacles
    states[2].obstacle = True          # S2 will be an obstacle
    states[9].obstacle = True          # S9 will be an obstacle
    
    ##-------------DEFINITION OF THE TRANSITION-COST MODEL------------------##
    states = TransCostModel(states, H, W)
    
    return states
     


    
    


           
    



