##----------------------------Function description--------------------------##
"""
This function is able to find a near-optimal solution of an FO-MDP using the 
algorthim Real Time Dynamic Programming. This algorithim suits the situations 
in which the automonous agent must respond quickly with an action as good as
possible before the timeout.

It can be seen as an asynchronous version of VI but it can also be described
within the frame of the Trial based Heuristic Tree Search (THTS),
because it is based on a sampling-nature. The algorithm will lauch 
"trials" until the temporal buget is reached. These trials sample greedy 
actions along the state-space performing bellman backups (to back propagate 
the information). Initially, the greedy action is absolutelly blind in 
recently discovered states. For this reason, an heuristic can be implmented in
order to guide the action selection.

Each trial continues until it reaches a terminal estate. In finite horizon MDP
it means that the last decision epoch has been completed. By contrast, in 
infinite horizon MDPs (goal oriented version) the terminal states can be 
either the goals or the dead-ends (Especial need for penalties here)

only relevant states will be updated. the exploration of the state-space may
not be complete. This means that the policy solution will not be computed for
the whole space state, given that the initial state is known.

Assets: -fast response with reasonably good actions
        -consistent against cyclic models (the trials are finite)
        -if the heuristic is admissible (lower bound) RTDP converges to V* at 
         least in relevant states.
        
        
Drawbacks: -extremely slow convergence. 
           -No optimality stopping criteria in the original algrothim. Here we
            will use one.

"""
 
def TRIAL(s, gamma):
    
    while not s.goal and not s.obstacle:
        
        # pick the best action and update the hash
        a = s.greedyAction(gamma)
        s.update(gamma)
        
        # stochastically simulate next state
        s = s.sampleNewState(a) 
        
        
    return
    
   
def RTDP(s0, gamma, maxTrials):
    
    s = s0                     
    n = 0
    while n < maxTrials :
        
        TRIAL(s, gamma)
        n += 1
              
    print("MDP RTDP: trials stopped, max number of trials reached")
    return
        
        
            