"""
This the declarative model for the first scenario to test and compare several
algorithms.

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
from ValueIteration import VI


##-----------------DEFINITION OF THE PLANNING DOMAIN------------------------##

#            -----------------
#            |S0 |S1 |S2 |S3 |
#            |S4 |S5 |S6 |S7 |
#            |S8 |S9 |S10|S11|
#            -----------------

H = 3                            # Height
W = 4                            # Width
n_obs = 2                        # Number of obstacles
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



##---------------DEFINITION OF THE TRANSITION-COST MODEL--------------------##
 
def Cost(listOfStates, dest):
    
    nominalCost = -0.05
    obstacleCost = -5
    goalCost = 0
    
    if listOfStates[dest].goal:
        return goalCost
    
    elif listOfStates[dest].obstacle:
        return obstacleCost
    
    else:
        return nominalCost
    
for s in states:
    
    # Stay action definition ------------------------------------------------
    if s.obstacle:
        s.transitions["Stay"] = {s.number: [1, -5]}
        
    elif s.goal:
        s.transitions["Stay"] = {s.number: [1, 0]}
        
    else:
        s.transitions["Stay"] = {s.number: [1, -0.05]}
        
        
    
    
    # NORTH action definition ------------------------------------------------    
    if s.obstacle:
        s.transitions["North"] = {s.number: [1, Cost(states, s.number)]} 
        
    elif s.goal:
        s.transitions["North"] = {s.number: [1, Cost(states, s.number)]}
    
    elif s.top:
        s.transitions["North"] = {s.number: [1, Cost(states, s.number)]}
       
    elif not s.top and s.left :
        #Compute destination states
        d1 = Grid2State(s.vPos-1, s.hPos, H, W)              #Upper state
        d2 =  Grid2State(s.vPos-1, s.hPos+1, H, W)           #up-right state
        
        s.transitions["North"] = {d1: [0.9, Cost(states, d1)],
                                  d2: [0.1, Cost(states, d2)]}
        
    elif not s.top and s.right :
        #Compute destination states
        d1 = Grid2State(s.vPos-1, s.hPos, H, W)              #Upper state
        d2 =  Grid2State(s.vPos-1, s.hPos-1, H, W)           #up-left state
        
        s.transitions["North"] = {d1: [0.9, Cost(states, d1)],
                                  d2: [0.1, Cost(states, d2)]}
        
    else:
        #Compute destination states
        d1 = Grid2State(s.vPos-1, s.hPos, H, W)              #Upper state
        d2 =  Grid2State(s.vPos-1, s.hPos-1, H, W)           #up-left state
        d3 =  Grid2State(s.vPos-1, s.hPos+1, H, W)           #up-right state 
        
        s.transitions["North"] = {d1: [0.8, Cost(states, d1)],
                                  d2: [0.1, Cost(states, d2)],
                                  d3: [0.1, Cost(states, d3)]}
        
    # SOUTH action definition ------------------------------------------------
    if s.obstacle:
        s.transitions["South"] = {s.number: [1, Cost(states, s.number)]} 
        
    elif s.goal:
        s.transitions["South"] = {s.number: [1, Cost(states, s.number)]}
    
    elif s.bottom:
        s.transitions["South"] = {s.number: [1, Cost(states, s.number)]}
       
    elif not s.bottom and s.left :
        #Compute destination states
        d1 = Grid2State(s.vPos+1, s.hPos, H, W)              #down state
        d2 = Grid2State(s.vPos+1, s.hPos+1, H, W)            #down-right state
        
        s.transitions["South"] = {d1: [0.9, Cost(states, d1)],
                                  d2: [0.1, Cost(states, d2)]}
        
    elif not s.bottom and s.right :
        #Compute destination states
        d1 = Grid2State(s.vPos+1, s.hPos, H, W)              #down state
        d2 = Grid2State(s.vPos+1, s.hPos-1, H, W)            #down-left state
        
        s.transitions["South"] = {d1: [0.9, Cost(states, d1)],
                                  d2: [0.1, Cost(states, d2)]}
        
    else:
        #Compute destination states
        d1 = Grid2State(s.vPos+1, s.hPos, H, W)              #down state
        d2 = Grid2State(s.vPos+1, s.hPos-1, H, W)            #down-left state
        d3 = Grid2State(s.vPos+1, s.hPos+1, H, W)            #down-right state 
        
        s.transitions["South"] = {d1: [0.8, Cost(states, d1)],
                                  d2: [0.1, Cost(states, d2)],
                                  d3: [0.1, Cost(states, d3)]}
    
    # East action definition ------------------------------------------------
    if s.obstacle:
        s.transitions["East"] = {s.number: [1, Cost(states, s.number)]} 
        
    elif s.goal:
        s.transitions["East"] = {s.number: [1, Cost(states, s.number)]}
    
    elif s.right:
        s.transitions["East"] = {s.number: [1, Cost(states, s.number)]}
       
    elif not s.right and s.top :
        #Compute destination states
        d1 = Grid2State(s.vPos, s.hPos+1, H, W)              #right state
        d2 = Grid2State(s.vPos+1, s.hPos+1, H, W)            #down-right state
        
        s.transitions["East"] = {d1: [0.9, Cost(states, d1)],
                                 d2: [0.1, Cost(states, d2)]}
        
    elif not s.right and s.bottom :
        #Compute destination states
        d1 = Grid2State(s.vPos, s.hPos+1, H, W)              #right state
        d2 = Grid2State(s.vPos-1, s.hPos+1, H, W)            #up-right state
        
        s.transitions["East"] = {d1: [0.9, Cost(states, d1)],
                                 d2: [0.1, Cost(states, d2)]}
        
        
    else:
        #Compute destination states
        d1 = Grid2State(s.vPos, s.hPos+1, H, W)              #right state
        d2 = Grid2State(s.vPos+1, s.hPos+1, H, W)            #down-right state
        d3 = Grid2State(s.vPos-1, s.hPos+1, H, W)            #up-right state 
        
        s.transitions["East"] = {d1: [0.8, Cost(states, d1)],
                                 d2: [0.1, Cost(states, d2)],        
                                 d3: [0.1, Cost(states, d3)]}
        
    # West action definition ------------------------------------------------
    if s.obstacle:
        s.transitions["West"] = {s.number: [1, Cost(states, s.number)]} 
        
    elif s.goal:
        s.transitions["West"] = {s.number: [1, Cost(states, s.number)]}
    
    elif s.left:
        s.transitions["West"] = {s.number: [1, Cost(states, s.number)]}
       
    elif not s.left and s.top :
        #Compute destination states
        d1 = Grid2State(s.vPos, s.hPos-1, H, W)              #left state
        d2 = Grid2State(s.vPos+1, s.hPos-1, H, W)            #down-left state
        
        s.transitions["West"] = {d1: [0.9, Cost(states, d1)],
                                 d2: [0.1, Cost(states, d2)]}
        
    elif not s.left and s.bottom :
        #Compute destination states
        d1 = Grid2State(s.vPos, s.hPos-1, H, W)              #left state
        d2 = Grid2State(s.vPos-1, s.hPos-1, H, W)            #up-left state
        
        s.transitions["West"] = {d1: [0.9, Cost(states, d1)],
                                 d2: [0.1, Cost(states, d2)]}
        
    else:
        #Compute destination states
        d1 = Grid2State(s.vPos, s.hPos-1, H, W)              #left state
        d2 = Grid2State(s.vPos+1, s.hPos-1, H, W)            #down-left state
        d3 = Grid2State(s.vPos-1, s.hPos-1, H, W)            #up-left state 
        
        s.transitions["West"] = {d1: [0.8, Cost(states, d1)],
                                 d2: [0.1, Cost(states, d2)],
                                 d3: [0.1, Cost(states, d3)]}   
       

##----------------------------------Solution--------------------------------##    

epsilon = 0.01
discount = 0.95
maxIter = 150
V0 = [0]*n_states

        
[policy , V, i, Res] = VI(states, discount, epsilon, maxIter, V0)