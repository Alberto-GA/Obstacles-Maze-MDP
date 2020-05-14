"""
his function is able to find a near-optimal solution of an FO-MDP using the 
algorthim Labeled - Real Time Dynamic Programming. This is the enhanced 
version of RTDP (See its code for further information).

This algorithm targets the same problems but with an improved convergence. If 
you are familiar with RTDP you will know that it lacks a convergence stopping
criterium. This is due to the fact that RTDP is supposed to work under time
pressure conditions, where the time out always arrives before convergence.

In fact RTDP can take from minutes to hours to the real convergence while the
policy is not changing quite a lot. This bad feature is the consequence of 
the privilege given to the most likely successors. These relevant succesors 
are vital for finding the best action quickly but the less likely successors 
are still needed for convergence.

What we can do in order to improve the convergence is to keep track of all the
states which have already converged and avoid visiting them again.

So the main idea of the algorithm is: launch trials as RTDP but these trials 
finish only in states labeled as solved. (initially only the goal is solved)
(I dont know what happen with dead-ends). And then, the check-solved procedure
is triggered in reversed order from the last unsolved back to S0, until I find
an unsolved state.

"""

def checkSolved(s, gamma, epsilon):
    
    rv = True                      # initialise the return value
    openStack = []                 # create a list with states still unchecked
    closedStack = []               # create a list with already checked states
    
    if not s.solved :              # if the state is not labeled solved
        
        openStack.append(s)        # add it to the list of unchecked states
        
        
    while not openStack == []:     # let's check start checking if there still
                                   # something to check
        
        last = len(openStack) -1   # take and remove the last element of the stack
        s = openStack[last]
        openStack.pop(last)                                                                         #OJO QUE HAGO EL POP EL ULTIMO HACIA ARRIBA
        
        closedStack.append(s)      # append that state to the already checked list
        
        # Check the residual
        if s.Residual(gamma) > epsilon:
            
            rv = False             # We have found an unconverged state.
                                   # This will finish the call to checkSolved
                                   # for each visited state during the trial
            continue               # But keep on exploring the openStack     
        
        # The following block only applies when a converged State is found
        # Expand the state and add its successors in the greedy graph just
        # to see if the have converged too.
        a = s.greedyAction(gamma)
        for successor in s.transitions[a].keys():
            
            if not successor.solved and successor not in (openStack + closedStack): 
                openStack.append(successor)  
                
    if rv :   #This means that all the checked states have converged
        
        # label relevant states
        for s in closedStack:
            s.solved = True
        
    else:     # the state or one of its successors have not converged
        
        # update states with residuals and ancestors
        while not closedStack ==  []:
            
            last = len(closedStack) -1   # take and remove the last element of the stack       #OJO QUE HAGO EL POP EL ULTIMO HACIA ARRIBA
            s = closedStack[last]
            closedStack.pop(last)
            
            s.update(gamma)
    
    return rv


def TRIAL_LRTDP(s, gamma, epsilon):
    
    # Each iteration, create an empty list to save all the states that have
    # been visited
    visited = []
    
    # The trial will continue until it reaches a solved-labeled state,
    # intially only the goal is solved.
    while not s.solved :
        
        # Append the current state to the visited list
        visited.append(s)                                                      #OJO CON LOS CICLOS
        
        # termination at goal and dead-ends.
        # in RTDP this was in the while condition because there wasn't any
        # other stopping criteria
        if  s.goal or s.obstacle :
            
            break
        
        # Now follow the same procedure as in RTDP 
        # pick the best action and update the hash
        a = s.greedyAction(gamma)
        s.update(gamma)
        
        # stochastically simulate next state
        s = s.sampleNewState(a)
    
    # once The trial has finished, try to label
    # the visited states in reverse order
    while not visited == [] :
        
        # take the last state of the list and remove it
        last = len(visited) -1
        s = visited[last]
        visited.pop(last)
        if not checkSolved(s, gamma, epsilon) :
            
            break # As soon as I find an unconverged state stop checking 
                  # because its predecessors won't have been converged neither
            
    
    return


def LRTDP(s0, gamma, epsilon):
    
    
    s = s0
    while not s.solved :                  # launch trials until the intial the
                                          # intial state is solved.
        
        TRIAL_LRTDP(s, gamma, epsilon)
    
    print("MDP LRTDP: trials stopped, epsilon-optimal policy found")
    return
        