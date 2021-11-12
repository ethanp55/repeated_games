import numpy as np
import random
import traceback
import importlib.util
import argparse
import glob
import os
import sys
import time

def process_arguments():
    parser = argparse.ArgumentParser(description='Play a repeated game match between two agents')
    parser.add_argument("agent1", help = "The file name for the first agents")
    parser.add_argument("agent2", help = "The file name for the second agents")
    parser.add_argument("-g, --game", dest='game', help = "Game to run on, otherwise runs on prisoner", default='coordination.txt')
    parser.add_argument("-p, --stop_prob", dest='stop_prob', type = float, help = "Specify the probability of stopping after each game", default = 0.005)
    parser.add_argument("-w, --write", dest='write', action='store_true', help = "Indicate that logfiles for games in the match should be saved to the logs directory", default = False)
    parser.add_argument("-v, --verbose", dest='verbose', action='store_true', help = "Indicate that the match should be run in verbose mode", default = False)
    return parser.parse_args()

def play_game(game, stop_prob, game_name, agents, save_logfile, verbose=False):
    """
    This will play a single repeated game between the given two agents
    Returns the average per round utility for each agents
    Parameters: 
        game: the game matrix that is being played
        stop_prob: the probability with which the game ends after each round
        game_name: the name of the game that is being played
        agents: an array of the two agents playing this game
        save_logfile: True/False - should the logfile be written out
        verbose: True/False - should we print details
    Returns: 
        A list of the average per round utility for each agents
    """

    #Create the logname and open the logfile if necessary
    logname = 'logs' + os.path.sep + 'GAME'
    agentstring = ''

    for i in range(len(agents)):
        logname = logname + '_' + agents[i].name
        agentstring = agentstring + 'Player ' + str(i) + ': ' + agents[i].name + '\n'

    if save_logfile:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        #Open the logfile
        logname = logname + '_' + game_name + '_' + timestr + '.log'
        logfile = open(logname, 'w')

        logfile.write(agentstring)
        logfile.write('GAME:' + str(game.tolist()))
        logfile.write('\n')
        logfile.write('ROUNDS:\n')

    #Tell the agents to start the game
    for i in range(len(agents)):
        agents[i].startGame(game)

    if verbose:
        print('Playing game between:')
        for a in agents:
            print('  Agent ', a.name)

    #Initialize stats about the game
    round_count = 0
    total_utility = np.zeros((1,2))
    done = False

    #Play the game until we end by random probability
    while not done:
        #Increment our round counter
        round_count += 1
        if verbose: 
            print('--Round--', round_count, '--BEGIN--')
    
        #Get the current actions from each agents
        actions = []
        for i in range(2):
            a = agents[i]
            try: 
                current_action = a.getAction(verbose)
            except Exception as e:
                print('ERROR for agents: ', a.name)
                print(e)
                traceback.print_exc()
                print(' playing random action')

                current_action = random.randint(0,1)

            actions.append(current_action)

        #Get the payoffs for the game 
        current_utilities = game[actions[0]][actions[1]][:]
        total_utility += current_utilities

        if verbose: 
            print('Actions chosen: ', actions)
            print('Utilities: ', current_utilities)
            print('------END-ROUND-----')

        #Tell the agents to update their histories
        for i in range(len(agents)):
            agents[i].update(i, actions)

        #Write current actions out to the logfile
        if save_logfile:
            logfile.write(str(actions))
            logfile.write('\n')
    
        #Toss the coin to see if we are done, or if the game continues
        if random.random() < stop_prob:
            done = True 

    if verbose:
        print('Game Ended after ', round_count, 'rounds')
        print('Total Utility: ', total_utility)

    if save_logfile:
        logfile.write('TOTAL UTILITY:' + str(total_utility.tolist()))
        logfile.write('\n' + str(round_count) + ' rounds were played.')
        logfile.close()

    #Return the average per round utility
    return total_utility/round_count

if __name__ == "__main__":
    
    #Get the arguments
    args = process_arguments()

    #Load the game
    game = np.loadtxt('games' + os.path.sep + args.game).reshape((2,2,2))

    #Load the agents
    all_agents = [args.agent1, args.agent2]
    agents = []

    for i in range(len(all_agents)):
        spec = importlib.util.spec_from_file_location('agents-' + str(i), "agents" + os.path.sep + all_agents[i])
        a = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(a)
        agents.append(a)
        i+= 1

    utilities = play_game(game, args.stop_prob, args.game[:-4], agents, args.write, args.verbose)
    print('Average (per round) utilities from single', args.game[:-4], 'game: ')
    for i in range(len(agents)):
        print('Agent: ', agents[i].name, ' : ', utilities[0][i])
    