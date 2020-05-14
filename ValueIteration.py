##-------------------------------LIBRARIES----------------------------------##

import operator

##----------------------------Function description--------------------------##
"""
This funciton applies the Value iteration algorithm to an input declarative 
model of an MDP in order to compute the policy solution.
inputs:
    decModel : it's the delarative model of the MDP. The data structure is a
               list of objects of type State. See StateClass for more info               
    gamma    : discount factor for infinite horizon MDP
    epsilon  : convergence criteria
    maxIter  : iterations budget
    V0       : initialization of the value function. (heuristic)

outputs:
    policy : this is the policy solution, the optimals actions that the agent 
             must make in all the states
    V      : Value function. The near-ptimal value of each state according to
             the near-optimal policy
    n      : Exit iteration
    Res    : Residuals of each state, just to check the convergence
    
WARNING -> the algorithm works well with infinite or finte horizon MDP and 
           their goal oriented version. Nevertheless, as a reminder the 
           dead-ends must be treated carefully due to the fact that the value
           function never converges in the dead-end states. A possible 
           improvement of this algorithim could consist in define a 
           finite-Penalty-SSP. (Mausam and Kolobov pg 58). But this is a
           particular customization for these kind of problems.
           
"""

def VI(decModel, gamma, epsilon, maxIter, V0):
    
    n_states   = len(decModel)                   # number of states
    policy     = [""] * n_states                 # policy solution
    V_old      = V0                              # initialization of the value function (heuristic)
    V          = [0]  * n_states                 # value function
    Res        = [0]  * n_states                 # Residual of each state
    n          = 0                               # iter counter
    optimality = 2*epsilon*gamma/(1-gamma)       # optimality convergence criterium
    
    while n < maxIter :                          # Refine V until the buget is reached
        
        for s in decModel:                       # Evaluate all the states
            
            # Initialization of state's BellMan operator.
            # Each state will have its own BM operator in each iteration
            # it will be a dictionary such that {"action": value}
            Bellman_operator = {}                 
            for a,dest in s.transitions.items(): # evaluate state's transitions
                
                # state.transitions reminder ->
                # a = "action"
                # dest = {s_prime : [probability, cost]}
                
                Bellman_operator[a] = 0
                for s_prime in dest.keys():      # Compute possible successors
                    
                    Bellman_operator[a] += dest[s_prime][0] * (dest[s_prime][1] +
                                                               gamma * V_old[s_prime.number])
            
            # For the state s, chose the greedy action in its
            # Bellman dictionary, update V and compute the residual       
            [policy[s.number],V[s.number]] = max(Bellman_operator.items(), key=operator.itemgetter(1))
            Res[s.number] = abs( V[s.number] - V_old[s.number] )
        
        # Once the value of all the states have been updated...
        # Compute iteration, and check exit conditions    
        n += 1
        
        if max(Res) < optimality:
            
            print("MDP Value Iteration: iterations stopped, epsilon-optimal policy found")
            return policy, V, n , Res
        
        elif n==maxIter:
            
            print("MDP Value Iteration: iterations stopped, max number of iteration reached")
            return policy, V, n, Res
        
        else:
            
            V_old = V
            V = [0]*n_states # don't know why but if you remove this, python 
                             # starts confusing V and V_old
        
       
        
