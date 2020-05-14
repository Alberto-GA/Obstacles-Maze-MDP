##-------------------------------LIBRARIES----------------------------------##

from SSP_obstaclesModel import declarativeModel
#from ValueIteration import VI
#from RealTimeDP import RTDP
#from LabeledRTDP import LRTDP
from UCT import UCT_like

##------------------------LOAD THE MODEL TO SOLVE---------------------------##

states = declarativeModel()

##-------------SOLVE THE PROBLEM WITH THE DESIRED ALGORITHM-----------------##

# Parameters
epsilon = 0.01
discount = 0.95



# Algorithm
# VI -------------------------------------------------------------------------
"""
maxIter = 150
n_states = len(states)
V0 = [0]*n_states
[policy , V, i, Res] = VI(states, discount, epsilon, maxIter, V0)
"""

# RTDP -----------------------------------------------------------------------
"""
n_states = len(states)
maxTrials = 10000
RTDP(states[0],discount, maxTrials)
sol = {}
for i in range(0,n_states):
    sol[str(states[i])] = [states[i].value, states[i].greedyAction(discount)]
"""
# LRTDP ----------------------------------------------------------------------
"""
n_states = len(states)
epsilon = 0.001
LRTDP(states[0],discount,epsilon)
sol = {}
for i in range(0,n_states):
    sol[str(states[i])] = [states[i].value, states[i].greedyAction(discount)]
"""    


# UCT ------------------------------------------------------------------------


maxTrials = 50
Graph = UCT_like(states[0], maxTrials)

"""
leer paper
crear github
intentar no instanciar todos los estados, sol cuando sea necesario
fix the closed LRTD
"""
