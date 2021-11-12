import os
import argparse
import glob
import sys
import importlib.util
import numpy as np
import time
import play_repeated_game as pg

def process_arguments():
    parser = argparse.ArgumentParser(description='Conduct a repeated game tournament between all agents on all games (in respective folders)')
    parser.add_argument("-g, --game", dest='game', help = "Game to run on, otherwise runs on all games", default=None)
    parser.add_argument("-n, --num", dest='num', type = int, help = "Specify the number of repetitions of the game to play", default = 5)
    parser.add_argument("-p, --stop_prob", dest='stop_prob', type = float, help = "Specify the probability of stopping after each game", default = 0.005)
    parser.add_argument("-w, --write", dest='write', action='store_true', help = "Indicate that logfiles for games in the match should be saved to the logs directory", default = False)
    parser.add_argument("-v, --verbose", dest='verbose', action='store_true', help = "Indicate that the match should be run in verbose mode", default = False)
    return parser.parse_args()

if __name__ == "__main__":
    #Get the arguments for this tournament
    args = process_arguments()

    #Get the games for this tournament 
    games = dict()
    
    if args.game is None:
        #Get all of the games from the games folder
        all_game_files = glob.glob('games' + os.path.sep + '*.txt')
    else:
        #Or just get the game they told us about
        all_game_files = ['games' + os.path.sep + args.game]

    print('Running a tournament.')
    print('  Tournament game files: ', all_game_files)

    for gf in all_game_files:
        #Load the game matrix
        gm = np.loadtxt(gf).reshape((2,2,2))
        #Get the game name
        gbfn = os.path.basename(gf)
        gn = gbfn[:-4]
        games[gn] = gm

    #Get all of the agents from the agents folder
    all_agent_files = glob.glob('agents' + os.path.sep + '*.py')
    #Display the agents file names and tournament information
    print('   Tournament agents: ', all_agent_files)

    print('   Tournament ARGS: ', args)

    if(args.verbose):
        print('Saving all log files to the logs folder')

    agents = []

    for i in range(len(all_agent_files)):
        spec = importlib.util.spec_from_file_location('agents-' + str(i), all_agent_files[i])
        a = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(a)
        agents.append(a)

    #Initialize information to store stats about the games
    N = len(agents)
    total_games_played = dict()
    total_total_utility = dict()
    total_crosstable = dict()

    for a in agents:
        total_games_played[a.name] = 0
        total_total_utility[a.name] = 0

    #Loop over each game in our list of games
    for game_name, game in games.items():        

        #Initialize stats for this game
        games_played = dict()
        total_utility = dict()
        crosstable = dict()

        for a in agents:
            games_played[a.name] = 0
            total_utility[a.name] = 0

        #Play each combination of agents for the number of repetitions of the game
        for a1 in agents:
            for a2 in agents:
                if a1 is not a2:
                    #Cross-table entries names for this matchup
                    x1 = a1.name + '-vs-' + a2.name 
                    x2 = a2.name + '-vs-' + a1.name
                    
                    #Store the utilities for this game
                    current_utilities = np.zeros((1,2))

                    print('Playing', args.num, ' ', game_name, 'games between ', a1.name, 'and', a2.name)

                    for i in range(args.num):
                        utilities = pg.play_game(game, args.stop_prob, game_name, [a1,a2], args.write, args.verbose)
                            
                        games_played[a1.name] += 1
                        total_utility[a1.name] += utilities[0][0]
                        games_played[a2.name] += 1
                        total_utility[a2.name] += utilities[0][1]
                        current_utilities += utilities

                    # Compute the average per game utility for each agents
                    current_utilities /= args.num
                    # Save in cross-table dictionary for this game
                    crosstable[x1] = current_utilities[0][0]
                    crosstable[x2] = current_utilities[0][1]


        #Compute summary statistics for this game.  Save them out 
        average_utility = dict()

        for a in agents:
            average_utility[a.name] = total_utility[a.name] / games_played[a.name]

        sorted_utility = sorted(average_utility.items(), key = lambda kv:kv[1],reverse=True) 

        #Write out the results for this game
        if args.write:
            tournament_log_string = "logs" + os.path.sep + 'TOURNAMENT-' + game_name + '-' + time.strftime("%Y%m%d-%H%M%S") + '.log'
            tlogfile = open(tournament_log_string, 'w')
            tlogfile.write('Tournment results for game: ' + game_name)
            tlogfile.write('\nSORTED AVERAGE UTILITY\n')
            for s in sorted_utility:
                tlogfile.write(str(s) + '\n')
            tlogfile.write('\nCROSSTABLE ENTRIES\n')
            for x in crosstable.items():
                tlogfile.write(str(x) + '\n')    
            tlogfile.write('\nGAMES PLAYED\n')
            for g in games_played.items():
                tlogfile.write(str(g) + '\n')
            tlogfile.close()
            print('Tournament log written to: ', tournament_log_string)

        for a in agents:
            total_games_played[a.name] += games_played[a.name]
            total_total_utility[a.name] += average_utility[a.name]

        for k, v in crosstable.items():
            if k not in total_crosstable:
                total_crosstable[k] = v
            else:
                total_crosstable[k] += v


    #Now that all games are done, save out the results for the whole tournament across all games
    sorted_total_utility = sorted(total_total_utility.items(), key= lambda kv:kv[1], reverse=True)

    if args.write:
        total_tournament_log_string = "logs" + os.path.sep + 'FINAL-TOURNAMENT-RESULTS-' + time.strftime("%Y%m%d-%H%M%S") + '.log'
        ttlf = open(total_tournament_log_string, 'w')
        ttlf.write('Final Tournament Results\n')
        ttlf.write('\nSORTED TOTAL (summed across games) AVERAGE (per game) UTILITY\n')
        for s in sorted_utility: 
            ttlf.write(str(s) + '\n')
        ttlf.write('\nTOTAL CROSS TABLE (summed across games, average utility)\n')
        for x in total_crosstable.items():
            ttlf.write(str(x) + '\n')
        ttlf.write('\nGAMES PLAYED\n')
        for g in total_games_played.items():
            ttlf.write(str(g) + '\n')
        ttlf.close()
        print('Total Tournament results written to: ', total_tournament_log_string)

    print('Final Tournament Results:\n\nUtilities:\n', sorted_utility)
    print('\nCrosstable:\n',total_crosstable)
    print('\nGames Played:\n', total_games_played)






