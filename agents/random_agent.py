import random

history = [0,0]     #Stores action count history of opponent
game = None         #Store the game being played
name = "Random"     #The name of this agents

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
    #Get random next action (out of 0 and 1)
    action = random.randint(0,1)
    if verbose:
        print('[Random Agent] Current opponent history: ', history)
        print('[Random Agent] Choosing random action: ', action)
    return action
