from random import seed
from random import random
import time
import itertools

seed(time.time() * time.time())


class state:
    """
    (n = number of colors, m = max number of colors of each ball, k = number of balls in a sequence)
    """
    def __init__(self, n: int, m: int, k: int):
        self.n = n
        self.m = m
        self.k = k
        # Sequence chosen by Player A at the start of the game (initialized randomly)
        self.final_state = self.generate_final_state()
        self.move_counter = 0

    def generate_final_state(self):
        possible_colors = []
        final_state = []

        for i in range(self.n):
            possible_colors.append(self.m)

        while len(final_state) < self.k:
            i = int(random() * self.n)
            if possible_colors[i] != 0:
                possible_colors[i] = possible_colors[i] - 1
                final_state.append(i)

        return final_state

    def is_final(self, state: list):
        if self.move_counter >= 2 * self.n:
            return -1
        if len(state) != len(self.final_state):
            return 0
        for i in range(len(state)):
            if state[i] != self.final_state[i]:
                return 0
        return 1
    def reset_move_counter(self):
        self.move_counter = 0


# Generate a move for player B
def generate_random_state(state: state):
    possible_colors = []
    random_state = []

    for i in range(state.n):
        possible_colors.append(state.m)

    while len(random_state) < state.k:
        i = int(random() * state.n)
        if possible_colors[i] != 0:
            possible_colors[i] = possible_colors[i] - 1
            random_state.append(i)

    state.move_counter += 1

    return random_state


def comp_states(state1: list, state2: list):
    common_colors = [x for x, y in zip(state1, state2) if x == y]
    return len(common_colors)

def correct_instance(state: state, instance: list):
    if len(instance) != state.k:
        return False
    for i in instance:
        if i >= state.n:
            return False
    possible_colors = []
    for i in range(state.n):
            possible_colors.append(state.m)
    for i in instance:
        possible_colors[i] = possible_colors[i] - 1
        if possible_colors[i] < 0:
            return False
    return True

def run_random_game(game_state: state):
    game_state.reset_move_counter()
    history = []
    while True:
        random_state = generate_random_state(game_state)
        history.append(random_state)
        print("Random state -", random_state, " - move number ", game_state.move_counter)
        # cheating:
        # if i == 6:
        #    random_state = A.final_state

        print("k = ", comp_states(random_state, game_state.final_state))

        if state.is_final(game_state, random_state) == -1:
            print("A won")
            break
        elif state.is_final(game_state, random_state) == 1:
            print("B won")
            break

# TODO: This is the bare minimum functionality
#   *nicer interface
#   *check for input longer than k
def run_player_game(game_state: state):
    game_state.reset_move_counter()
    history = []
    while True:
        print("Input color (0 to ", game_state.n - 1, "), ", game_state.m,"balls each with the length of", game_state.k, ":")
        current_state = [int(i) for i in input().split()]
        #current_state = generate_random_state(game_state)
        # cheating:
        # if i == 6:
        #    current_state = A.final_state
        if correct_instance(game_state, current_state):
            history.append(current_state)
            game_state.move_counter = game_state.move_counter + 1
            print("Current state -", current_state, " - move number ", game_state.move_counter)

            print("k = ", comp_states(current_state, game_state.final_state))

            if state.is_final(game_state, current_state) == -1:
                print("A won")
                break
            elif state.is_final(game_state, current_state) == 1:
                print("B won")
                break
        else:
            print("Wrong Instance")


def generate_all_states(game_state: state):
    possible_colors = []

    for i in range(game_state.n):
        possible_colors.append(i)

    #All states
    all_possible_states = list(itertools.product(possible_colors, repeat=game_state.k))

    #All possible states
    states_count = len(all_possible_states)
    i = 0
    while i < states_count:
        for j in all_possible_states[i]:
            if all_possible_states[i].count(j) > game_state.m:
                all_possible_states.remove(all_possible_states[i])
                i = i - 1
                states_count = states_count - 1
                break
        i = i + 1
    return all_possible_states

def possible_choices(n: int, k: int):
    if k == 0:
        return []

    all_possible_choices = list(itertools.permutations(range(n),k))

    possible_choices = []
    for i in all_possible_choices:
        i = list(i)
        i.sort(key = lambda x: x)
        if not i in possible_choices:
            possible_choices.append(i)

    return possible_choices

def eliminate_choices(S: list, possible_choices: list, choice: list):
    new_S = []

    for i in S:
        found = False
        good = True
        for j in possible_choices:
            is_good = True
            for k in j:
                if i[k] != choice[k]:
                    is_good = False
            if is_good:
                if not found:
                    found = True
                else:
                    #print(j, i)
                    good = False
        if good and found:
            new_S.append(i)
    if len(possible_choices) == 0:
        for i in S:
            good = True
            for j in range(len(choice)):
                if i[j] == choice[j]:
                    good = False
            if good:
                new_S.append(i)

    return new_S

def minimax(S:list, all_S: list):
    scores = [0] * len(all_S)
    for i in all_S:
        if not i in S:
            found = [0] * len(all_S[0])
            for j in S:
                feedback = comp_states(i, j)
                found[feedback] = found[feedback] + 1
            scores[all_S.index(i)] = max(found)

    minim = min(scores)

    guess = []

    for i in all_S:
        if scores[all_S.index(i)] == minim:
            guess.append(i)

    return guess

def choose_possible(S:list, possible: list):
    choices = list(set(S).intersection(possible))
    if len(choices) > 0:
        return choices[int(random() * len(choices))]
    return possible[int(random() * len(possible))]

def next_guess(S: list, all_S: list):
    code = choose_possible(S, minimax(S, all_S))

    all_S.remove(code)

    return code

def guess_algorithm(game_state: state):
    game_state.reset_move_counter()
    S = generate_all_states(game_state)
    all_S = generate_all_states(game_state)

    while game_state.move_counter < game_state.n * 2:
        guess = next_guess(S, all_S)
        game_state.move_counter = game_state.move_counter + 1

        match = comp_states(guess, game_state.final_state)
        if match == game_state.k:
            return guess, game_state.move_counter

        S = eliminate_choices(S, possible_choices(game_state.k, match), guess)
    return -1

A = state(8, 1, 4)

print(guess_algorithm(A))
print("Final state -", A.final_state)

