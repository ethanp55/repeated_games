import numpy as np

history = [1,1]             #Stores action count history of opponent
game = None                 #Store the game being played
name = "FictitiousPlayer"   #The name of this agents

def startGame(g):
    """ 
    Called when a new game begins. 
    Agent should reset any information
    Parameters: 
        g - the game matrix which will be played
    """ 
    global game  
    global history
    game = g
    history = [1,1]

def update(my_index, actions):
    """
    Called after each round in the game. 
    Parameters: 
        my_index : 0 or 1, the index of this agents
        actions : a vector of actions that were selected
    """
    global history
    opp_index = not my_index
    history[actions[opp_index]] += 1

def getBestResponse():
    """
    Custom function for this agents.  Will compute the
    best resoponse to the mixed strategy represented by the 
    action count history
    """
    #Computer mixed strategy for opponent from history
    p = np.array([h/sum(history) for h in history])

    #Compute our EV for each action, relative to their action distribution
    # This assumes we are agents 1, but the game is symmetric, so
    # it shouldn't matter
    ev = game[:,:,0].dot(p)

    #Return our best response action
    return np.argmax(ev)

def getAction(verbose=False):
    """
    Called in each round to get this agents's next action
    Parameters: 
        verbose: True/False - should print out details?
    Returns: 
        action: 0/1 - next action in the repeated game
    """
    #Get best response to opponent's mixed strategy (inferred from history)
    action = getBestResponse()  
    if verbose:
        print('[Fictitious Player] Current opponent history: ', history)
        print('[Fictitious Player] Choosing FP BR action: ', action)
    return action
