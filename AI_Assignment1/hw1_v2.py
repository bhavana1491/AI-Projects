import sys
import copy

Dict = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
neg_infinity = -999999999
infinity = 999999999
#alpha = neg_infinity
#beta = infinity
max_list ={}

class node:
    def __init__(self,depth,alpha,beta,state):
        self.depth = depth
        self.alpha = alpha
        self.beta = beta
        self.state = state

weighted_arr = [
    [99, -8, 8, 6, 6, 8, -8, 99],
    [-8, -24, -4, -3, -3, -4, -24, -8],
    [8, -4, 7, 4, 4, 7, -4, 8],
    [6, -3, 4, 0, 0, 4, -3, 6],
    [6, -3, 4, 0, 0, 4, -3, 6],
    [8, -4, 7, 4, 4, 7, -4, 8],
    [-8, -24, -4, -3, -3, -4, -24, -8],
    [99, -8, 8, 6, 6, 8, -8, 99]
]


move_directions = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
max_nodes = []

def evaluation(state, player):
    X_Sum = 0
    O_Sum = 0
    for i in range(0, 7):
        for j in range(0, 7):
            if state[i][j] == 'X':
                X_Sum = X_Sum + weighted_arr[i][j]

            else:
                if state[i][j] == 'O':
                    O_Sum = O_Sum + weighted_arr[i][j]

    if (player == 'X'):
        return X_Sum - O_Sum

    if (player == 'O'):
        return O_Sum - X_Sum


def cutoff_Test(d):
    if d == 0:
        return 1
    else:
        return 0




def alpha_beta_search(state, depth, player):
    print 'Node,Depth,Value,Alpha,Beta'
    value = Max_Val(state, neg_infinity, infinity, depth)
    return value


def Max_Val(state, alpha, beta, depth):
    global next_state
    '''for i in range(8):
        for j in range(8):
            print state[i][j],
        print'''
    if cutoff_Test(depth):
        return evaluation(state, player)
    value = neg_infinity
    available_moves = getValidMoves(state, player)
    for i,j in available_moves:
        max_nodes.append(Dict[j]+str(i+1))
    #print max_nodes
    for (a,s) in available_moves:
        #print available_moves
        next_state = get_updated_state(a,s,copy.deepcopy(state), player)

        #max_depth = depth - 1
        #max_states.push((max_node,max_depth))
        '''for i in range(8):
            for j in range(8):
                print next_state[i][j],
            print'''
        #print max_states.peek()
        value = max(value, Min_Val(next_state, alpha, beta, depth-1))

        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value


def Min_Val(state, alpha, beta, depth):
    '''for i in range(8):
        for j in range(8):
            print state[i][j],
        print'''
    opponent = player_opponent(player)
    if cutoff_Test(depth):
        return evaluation(state, opponent)
    value = infinity
    available_moves = getValidMoves(state, opponent)
    #print available_moves
    for (a, s) in available_moves:
        #print available_moves
        next_state = get_updated_state(a, s, copy.deepcopy(state), opponent)
        min_node = Dict[s]+str(a+1)
        min_depth = depth+1
        #min_states.push((min_node,min_depth))
        #print min_states.peek()
        '''for i in range(8):
            for j in range(8):
                print next_state[i][j],
            print'''
        value = min(value, Max_Val(next_state, alpha, beta, depth-1))
        #print max_states.peek()
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value


def get_updated_state(x,y, state, player):

    global flips
    flips = checkValidMove(state, player, x, y)
    state[x][y] = player
    # print flips
    if flips == False:
        return state


    for i, j in flips:
        state[i][j] = player
    return state


def getValidMoves(state, player):
    valid_moves = []

    for i in range(8):
        for j in range(8):
            if checkValidMove(state, player, i, j):
                valid_moves.append([i, j])
    return valid_moves


def checkValidMove(state, player, i, j):
    if state[i][j] != '*' or not isValidSquare(i, j):
        return False

    state[i][j] = player

    opponent = player_opponent(player)

    valid_flips = []

    for x, y in move_directions:

        x_step = i
        y_step = j

        x_step = x_step + x
        y_step = y_step + y

        if isValidSquare(x_step, y_step) and state[x_step][y_step] == opponent:
            x_step += x
            y_step += y

            while state[x_step][y_step] == opponent:
                x_step += x
                y_step += y
                if not isValidSquare(x_step, y_step):  # break out of while loop, then continue in for loop
                    break
            if not isValidSquare(x_step, y_step):
                continue
            if state[x_step][y_step] == player:
                while True:
                    x_step -= x
                    y_step -= y
                    if x_step == i and y_step == j:
                        break
                    valid_flips.append([x_step, y_step])

    state[i][j] = '*'
    if not len(valid_flips) == 0:
        return valid_flips
    return False


def isValidSquare(i, j):
    if 0 <= i <= 7 and 0 <= j <= 7:
        return True
    else:
        return False


def player_opponent(player):
    if player == 'X':
        opponent = 'O'
    else:
        if player == 'O':
            opponent = 'X'
    return opponent


def main():
    file = open('input.txt', 'r')

    contents = file.read().splitlines();

    global depth, player, opponent
    player = contents[0]
    depth = int(contents[1])
    opponent = player_opponent(player)

    arr = []
    for i in range(2, len(contents)):
        arr.append(list(contents[i]))

    #print arr

    # print evaluation(arr,player)

    #print getValidMoves(arr,player_opponent(player))


    alpha_beta_search(arr,depth,player)
    #print get_updated_state(2,3,arr,player)


main()
