history = [0,0]     #Stores action count history of opponent
game = None         #Store the game being played
name = "Constant0"  #The name of this agents

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
    history = [0,0]

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

def getAction(verbose=False):
    """
    Called in each round to get this agents's next action
    Parameters: 
        verbose: True/False - should print out details?
    Returns: 
        action: 0/1 - next action in the repeated game
    """
    action = 0
    if verbose:
        print('[Constant 0] Current opponent history: ', history)
        print('[Constant 0] Choosing action: ', action)
    return action
