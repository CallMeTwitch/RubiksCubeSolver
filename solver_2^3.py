# #########################
# 2x2x2 Optimal Rubik's 
# Cube Solver. Can solve 
# any 2^3 cube in 11 moves 
# or less.
# 
# Cube Index Format:
# 
#         0,  1
#         2,  3
# 4,  5,  6,  7,  8,  9,  10, 11
# 12, 13, 14, 15, 16, 17, 18, 19
#         20, 21
#         22, 23
# 
# Code written for a 
# entertainment.
# #########################

from matplotlib import pyplot as plt
from random import choice 
from PIL import Image

# Moves - Right Face Clockwise, Top Face Clockwise & Front Face Clockwise, Respectively
permutations = [
    {1:7, 3:15, 7:21, 8:16, 9:8, 10:3, 15:23, 16:17, 17:9, 18:1, 21:18, 23:10},
    {0:2, 1:0, 2:3, 3:1, 4:6, 5:7, 6:8, 7:9, 8:10, 9:11, 10:4, 11:5},
    {2:13, 3:5, 5:20, 6:14, 7:6, 8:2, 13:21, 14:15, 15:7, 16:3, 20:16, 21:8}
]

# Notation for Moves (o - 90deg, 2 - 180deg, p - 270deg), (R - Right Face, U - Top Face, F = Front Face)
turns = ['o ', '2 ', 'p ']
moves = 'RUF'

# Move Function
def permute(state, action):
    return ''.join([state[q] if q not in permutations[action] else state[permutations[action][q]] for q in range(len(state))])

# Scramble Function
def shuffle(state):
    for _ in range(100):
        state = permute(state, choice(range(len(permutations))))
    return state

# Solve Function
def solve(scramble, solution):
    prev_start, prev_end = set(), set()
    current_start, current_end = {scramble: ''}, {solution: ''}

    # Maximum Number of Moves to Solve Pocket Cube is 11 (11 // 2 + 1 = 6)
    for _ in range(6):

        next_start = {}
        # Iterate States
        for state in current_start:
            # If in both Dictionaries: Return
            if state in current_end:
                return (current_start[state] + current_end[state]).split()

            # Iterate Moves
            for move in range(3):
                current_state = state
                # Iterate Degrees
                for turn in range(3):
                    current_state = permute(current_state, move)
                    # If State New: Append to New Dictionary
                    if current_state not in prev_start:
                        next_start[current_state] = current_start[state] + moves[move] + turns[turn]
        # Redefine
        prev_start, current_start = set(current_start), next_start

        next_end = {}
        # Iterate States
        for state in current_end:
            # If in both Dictionaries: Return
            if state in current_start:
                return (current_start[state] + current_end[state]).split()
            
            # Iterate Moves
            for move in range(3):
                current_state = state
                # Iterate Degrees
                for turn in range(3):
                    current_state = permute(current_state, move)
                    # If State New: Append to New Dictionary
                    if current_state not in prev_end:
                        next_end[current_state] = moves[move] + turns[2 - turn] + current_end[state]
        # Redefine
        prev_end, current_end = set(current_end), next_end

# Follow Instructions
def do(instructions, scramble):
    for q in instructions:
        move, turn = q
        move, turn = moves.index(move), turns.index(turn + ' ')
        for _ in range(turn + 1):
            scramble = permute(scramble, move)
        show(scramble)
    plt.close()
    return scramble

# Function to Show
def show(state):
    plt.ion()
    image = Image.new('RGB', (8, 6))

    # Make Net
    layer1 = [0, 0] + list(state[:2]) + [0, 0, 0, 0]
    layer2 = [0, 0] + list(state[2:4]) + [0, 0, 0, 0]
    layer3 = list(state[4:12])
    layer4 = list(state[12:20])
    layer5 = [0, 0] + list(state[20:22]) + [0, 0, 0, 0]
    layer6 = [0, 0] + list(state[22:24]) + [0, 0, 0, 0]

    # Letter to Colour
    d = {0: (0, 0, 0), 'W': (255, 255, 255), 'B': (0, 0, 255), 'R': (255, 0, 0), 'G': (0, 255, 0), 'O': (255, 127, 0), 'Y': (255, 255, 0)}

    # Map ^
    map = [layer1, layer2, layer3, layer4, layer5, layer6]
    grid = []
    for layer in map:
        for val in layer:
            grid.append(d[val])
    
    # Show
    image.putdata(grid)
    image = image.resize((800, 600), resample = Image.NEAREST)
    image = plt.imshow(image)
    plt.show()
    plt.pause(0.5)
    plt.clf()

# Run
solved = 'RRRRBBWWGGYYBBWWGGYYOOOO'
scramble = shuffle(solved)
instructions = solve(scramble, solved)
print(instructions)
scramble = do(instructions, scramble)