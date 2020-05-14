
import math


#----------------------------------------------------------------------------#

def Grid2State(i, j, H, W):
    # This function returns the state (key in the states dictionary) from the
    # grid format.
    # Inputs: i,j = index in the grid format
    #         H = number of rows of the grid
    #         W = number of columns of the grid
    
    if i < H and j < W:
        
        return i*W +j
    
    else:
        
        return "Wrong Input arguments"
     
  
#----------------------------------------------------------------------------#    
  
def State2Grid(index, H, W):
    # This function returns the position in the grid map in matrix format (i,j)
    # Inputs: state = index in the State list
    #         H = number of rows of the grid
    #         W = number of columns of the grid
    
    
    if index >= 0  and  index < H*W:
       
        i = math.ceil((index + 1 )/W) - 1
        j = index - W*i
        
        return i, j
    
    else:
        
        return "Wrong Input arguments"