"""
This algorithm is an adptation of the classical UCT algorithm. It is based on 
RTDP. Credits to Caroline Chanel



"""
import math
import operator
#----------------------------------------------------------------------------#
"""
The Rollout function is used to initialise the Q-value of a new node in the 
Graph. It basically returns an estimation of the long term cost/reward starting
from the child "s".
Note that the rollout do not need to end in the goal.
"""
def Rollout(s):
    
    depth = 5       # Define the depth parameter, how deep do you want to go?
    nRollout = 0    # initialise the rollout counter
    payoff = 0      # initialise the cummulative cost/reward
    while nRollout < depth:
        # The rollouts progress with random actions -> sample an action
        a = s.SampleAction()
        print(a)
        # Sample a state according to P(s'|s,a)
        successor = s.sampleNewState(a)
        print(successor)
        # Compute the inmediate cost/reward and update the payoff
        payoff += s.transitions[a][successor][1]
        print(payoff)
        # update the current state with the sampled successor
        s = successor
        # increase the rollout counter
        nRollout += 1
    return payoff

#----------------------------------------------------------------------------#    
"""
The action selection method is the heart of UCT. It is the way the algorithm 
deals with the exploration-exploitation dilemma. Namely, UCT takes the ideas 
of bandit problems and applies the UCB formula to solve the conflict. In this
formula there is a term that votes for exploitation of the best current policy.
By contrast, the other term is devoted to exploring less visited nodes.

It receives the current Graph as input because this function doesn't modify 
the graph.

"""
def ActionSelection(s,G):
    c = 10           # Exploration coefficient 
    UCB = {}         # Dictionary to save the result of UCB for each action
    
    for a in  G[s].keys():          # UCB formula
        if not a=="N":              # a key of this dictionary is not an action
            UCB[a] = G[s][a]["Q-value"] + c * math.sqrt(math.log(G[s]["N"])/G[s][a]["Na"])

    # choose the action that maximize the UCB formula    
    a_UCB = max(UCB.items(), key=operator.itemgetter(1))[0]
    return a_UCB
    
#----------------------------------------------------------------------------#   
def UCT_Trial(s):
    
    global G           # Make sure that I have access to the graph
    K = -5             # Internal parameter -> asociated cost to dead-ends
    
    # 1) CHECK IF THE STATE IS TERMINAL---------------------------------------
        # as a reminder: in finite horizion MDP terminal means that the final
        # decision epoch has been reached. In infinte horizon (disc. reward) 
        # MDP, the terminal states are the goals and the dead-ends.
        
    if s.goal : return 0               # No cost to reach the goal
    elif s.obstacle: return K          # Penalty for dead-ends
        
    # 2) CHECK IF THE STATE IS ALREADY IN THE GRAPH---------------------------
    if s not in G:
        
        # create a new node in the graph if this is a new state
        G[s] = {}             # intialise node's dictionary
        G[s]["N"] = 1         # Count the first visit to the node                            ESTO NO ESTA EN EL CODIGO
        
        # initialise the Q-values based on rollouts
        # note that all the possible actions are tested
        # note that the childs are not created in the graph
        aux = []              # empty list to ease the maximization
        for a in s.transitions.keys():
            
            # Sample a successor according to the generative model
            successor = s.sampleNewState(a)
            print("successor pre rollout",successor)
            
            # the Qvalue is the inmediate cost/reward plus the long term
            # cost/reward that is estimated through a rollout
            G[s][a]={}
            G[s][a]["Q-value"] = s.transitions[a][successor][1] + Rollout(successor)
            aux.append(G[s][a]["Q-value"])  
            
            # Register the visit for this pair s-a
            G[s][a]["Na"]= 1
        
        rv = max(aux)        # the return value is the max Q(s,a)
        aux = []             # clear the auxiliary list
        return rv
    
    # 3) EXPAND THE NODE IF IT'S ALREADY IN THE GRAPH ------------------------
        # To expand a node, UCT applies the action selection  
        # strategy that is based on the UCB formula    
    a_UCB = ActionSelection(s,G)
    
    # 4) SAMPLE A CHILD FOLLOWING PLAYING THIS ACTION ------------------------
    successor = s.sampleNewState(a_UCB)
    
    # 6) UPDATE THE COUNTERS -------------------------------------------------
    G[s]["N"] += 1
    G[s][a_UCB]["Na"] += 1   # I've reversed the order to solve cycles.....let's see
    
    # 5) WHAT IS THIS? -------------------------------------------------------
    QvaluePrime =  s.transitions[a_UCB][successor][1] + UCT_Trial(successor)  
    """
    Problems here! If UCT_Trial(s*) tells me that a_UCB is "stay" the successor
    will be s* (not only the problem of "stay" imagine playing "north" in 
    the border...). This means that I will call again UCT_Trial(s*) that will
    give me the same a_UCB and consequently, I will enter an infinite loop.
    
    how to solve? if the successor is the same then change the action? do I 
    have to cvhange ActionSelection method or solve it at this level....
    
    """      
    

    
    # 7) UPDATE THE Q-VALUE OF THE PAIR (s,a_UCB)-----------------------------
    G[s][a_UCB]["Q-value"] += (QvaluePrime + G[s][a_UCB]["Q-value"]) / G[s][a_UCB]["Na"]
    
    return QvaluePrime       
    
#----------------------------------------------------------------------------#    
"""
This is the skeleton of the UCT: it relies on the UCT_Trial mnethod wich will
update and refine the information in G, a global variable which represents
the current partial tree. The desired architecture for this variable is:
    
    G = { s1: {a1 : {"Q-value" : current estimation for Q(s1,a1)
                        "Na"   : number of times we have played a1 in s1}
               a2 : {...}
               N  : Number of times this State has been visited} 
         
         s2:{...}
         }
"""
def UCT_like(s0, maxTrials):
    
    nTrial = 0                         # initialize the trial counter
    global G                           # make a global variable so that all 
                                       # the functions can modify it
    G = {}                             # initialize a graph
    while nTrial < maxTrials :         # perform trials while possible
        
        UCT_Trial(s0)
        nTrial += 1
        
    return G     