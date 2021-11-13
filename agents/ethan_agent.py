import random

prev_actions = [0, 0]
game = None
name = "Ethan Pedersen"
coop_action_pairs = None
two_optimal_actions = False
no_optimal_actions = False
my_idx = 0
opp_idx = not my_idx


def _get_coop_action_pairs():
    cells = {(game[0, :2], 0, 0), (game[0, 2:], 0, 1), (game[1, :2], 1, 0), (game[1, 2:], 1, 1)}
    optimal_cells = []
    filtered_optimal_cells = []

    for cell, p1_action, p2_action in cells:
        p1_reward, p2_reward = cell
        other_cells = cells.difference({cell})
        optimal = True

        for other_cell, other_p1_action, other_p2_action in other_cells:
            other_p1_reward, other_p2_reward = other_cell

            if other_p1_reward > p1_reward and other_p2_reward > p2_reward:
                optimal = False
                break

        if optimal:
            optimal_cells.append((cell, p1_action, p2_action))

    optimal_rewards = [cell for cell, _, _ in cells]
    max_sum = sum(max(optimal_rewards, key=lambda x: sum(x)))

    for cell, p1_action, p2_action in cells:
        if sum(cell) == max_sum:
            filtered_optimal_cells.append((p1_action, p2_action))

    return filtered_optimal_cells


def startGame(g):
    global game
    global prev_actions
    global coop_action_pairs
    global two_optimal_actions

    game = g
    prev_actions = [0, 0]
    coop_action_pairs = _get_coop_action_pairs()
    two_optimal_actions = len(coop_action_pairs) > 1


def update(my_index, actions):
    global prev_actions
    global my_idx
    global opp_idx

    my_idx = my_index
    opp_index = not my_index
    prev_actions[my_index] = actions[my_index]
    prev_actions[opp_index] = actions[opp_index]


def getAction(verbose=False):
    my_prev_action = prev_actions[my_idx]
    opp_prev_action = prev_actions[opp_idx]

    if no_optimal_actions:
        action = random.randint(0, 1)

    elif two_optimal_actions:
        player_indices = sorted([my_idx, opp_idx])
        sorted_prev_actions = [prev_actions[i] for i in player_indices]

        action = my_prev_action if tuple(sorted_prev_actions) in coop_action_pairs else not my_prev_action

    else:
        coop_pair = coop_action_pairs[0]
        opp_prev_action_was_coop = coop_pair[opp_idx] == opp_prev_action

        action = coop_pair[my_idx] if opp_prev_action_was_coop else not coop_pair[my_idx]

    if verbose:
        print('[Constant 1] Current opponent history: ', prev_actions)
        print('[Constant 1] Choosing action: ', action)

    return action
