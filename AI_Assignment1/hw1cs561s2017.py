import sys
import copy

Dict = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
neg_infinity = -999999999
infinity = 999999999
global max_list,st_list,st_str,best_val_list
max_list =[]
st_list =[]
st_str = ""
best_val_list={}
best_state=[]
O_file = open('output.txt','w')
class Stack(object):

   def __init__(self):
      self.items = []

   def push(self, item):
      self.items.append(item)

   def pop(self):
       return self.items.pop()

   def peek(self):
       return self.items[-1]

   def isEmpty(self):
       return len(self.items) == 0


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
global max_states,min_states
max_states = Stack()
min_states = Stack()
def evaluation(state, player):
    X_Sum = 0
    O_Sum = 0
    for i in range(0, 8):
        for j in range(0, 8):
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
    if d == dep:
        return 1
    else:
        return 0


def alpha_beta_search(state, depth, player):
    moves = getValidMoves(state, player)
    if len(moves) == 0 :
        for i in range(8):
            st_list = state[i]
            st_str = "".join(map(str,st_list))
            O_file.write(st_str)
            O_file.write("\n")
    O_file.write('Node,Depth,Value,Alpha,Beta')
    O_file.write("\n")
    max_states.push(['root',str(depth),'-Infinity','-Infinity','Infinity'])
    p_max_list = max_states.pop()
    p_max_str = ",".join(map(str,p_max_list))
    max_states.push((p_max_list))
    O_file.write(p_max_str)
    O_file.write("\n")
    value = Max_Val(state, neg_infinity, infinity, depth)
    if any(best_val_list):
        best_filp = max(best_val_list.iterkeys(), key=(lambda key: best_val_list[key]))
        i=best_filp[0]
        j=best_filp[1]
        new_state = get_updated_state(j, i, state, player)
        O_file.close()
        file = open('output.txt', 'r')
        text = file.read()
        file.close()
        file = open('output.txt', 'w')
        for i in range(8):
            st_list = new_state[i]
            st_str = "".join(map(str, st_list))
            file.write(st_str)
            file.write("\n")
        file.write(text)
        file.close()
    return value


def Max_Val(state, alpha, beta, depth):
    global next_state
    if cutoff_Test(depth):
        return evaluation(state, player)
    value = neg_infinity
    available_moves = getValidMoves(state, player)
    new_max_list = max_states.pop()
    new_max_node = new_max_list[0]
    max_states.push(new_max_list)
    if len(available_moves) == 0 and new_max_node == 'root':
        max_value = 'Infinity'
        max_states.push(('pass', str(depth+1), str(max_value), str(alpha), str(beta)))
        new_max_list = max_states.pop()
        new_max_list = ['-Infinity' if x == '-999999999' else x for x in new_max_list]
        new_max_list = ['Infinity' if x == '999999999' else x for x in new_max_list]
        max_states.push(new_max_list)
        p_max_list = max_states.pop()
        p_max_str = ",".join(map(str, p_max_list))
        max_states.push((p_max_list))
        O_file.write(p_max_str)
        O_file.write("\n")

        value = max(value, Min_Val(state, alpha, beta, depth + 1))
        if value >= beta:
            return value
        alpha = max(alpha, value)
        new_min_list = min_states.pop()
        new_min_node = new_min_list[0]
        min_states.push(new_min_list)
        if new_min_node == 'pass':
            p_min_list = min_states.pop()
            p_min_str = ",".join(map(str, p_min_list))
            min_states.push((p_min_list))
            O_file.write(p_min_str)
            O_file.write("\n")
        new_min_list = min_states.pop()
        if new_min_list[0] != 'pass':
            new_max_list = max_states.pop()
            new_max_list='root', str(depth), str(value), str(alpha), str(beta)
            new_max_list = ['-Infinity' if x == '-999999999' else x for x in new_max_list]
            new_max_list = ['Infinity' if x == '999999999' else x for x in new_max_list]
            max_states.push(new_max_list)
            p_max_list = max_states.pop()
            p_max_str = ",".join(map(str, p_max_list))
            max_states.push((p_max_list))
            O_file.write(p_max_str)
            O_file.write("\n")
        if new_min_list[0] == 'pass':
            new_max_list = max_states.pop()
            new_max_list[2] = str(value)
            new_max_list[4] = str(value)
            max_states.push(new_max_list)
            p_max_list = max_states.pop()
            p_max_str = ",".join(map(str, p_max_list))
            max_states.push((p_max_list))
            O_file.write(p_max_str)
            O_file.write("\n")
            alpha = max(value,alpha)
            new_max_list = 'root',str(depth),str(value),str(alpha),str(beta)
            new_max_list = ['Infinity' if x == '999999999' else x for x in new_max_list]
            max_states.push(new_max_list)
            p_max_list = max_states.pop()
            p_max_str = ",".join(map(str, p_max_list))
            max_states.push((p_max_list))
            O_file.write(p_max_str)
            O_file.write("\n")
    elif len(available_moves) == 0:
        max_depth = depth + 1
        max_value = 'Infinity'
        max_states.push(('pass',str(max_depth), str(max_value), str(alpha), str(beta)))
        if max_depth == dep:
            new_max_list = max_states.pop()
            max_val = evaluation(state, player)
            new_max_list = new_max_list[0], str(max_depth), str(max_val), str(alpha), str(beta)
            max_states.push(new_max_list)
            new_max_list = max_states.pop()
            new_max_list = ['-Infinity' if x == '-999999999' else x for x in new_max_list]
            new_max_list = ['Infinity' if x == '999999999' else x for x in new_max_list]
            max_states.push(new_max_list)
            p_max_list = max_states.pop()
            p_max_str = ",".join(map(str, p_max_list))
            max_states.push((p_max_list))
            O_file.write(p_max_str)
            O_file.write("\n")
            alpha = max(max_val, alpha)
            new_min_list = min_states.pop()
            new_min_list = new_min_list[0], str(depth), str(max_val), str(alpha), str(beta)
            min_states.push(new_min_list)
            new_min_list = min_states.pop()
            new_min_list = ['Infinity' if x == '999999999' else x for x in new_min_list]
            min_states.push(new_min_list)
            p_min_list = min_states.pop()
            p_min_str = ",".join(map(str, p_min_list))
            min_states.push((p_min_list))
            O_file.write(p_min_str)
            O_file.write("\n")
        max_states.pop()

        value = max(value, Min_Val(state, alpha, beta, depth + 1))

        if value >= beta:
            return value
        alpha = max(alpha, value)
        return value

    for (a, s) in available_moves:
        next_state = get_updated_state(a,s,copy.deepcopy(state), player)
        max_node = Dict[s]+str(a+1)
        max_depth = depth + 1
        max_val = 'Infinity'
        max_list=max_node,str(max_depth),str(max_val),str(alpha),str(beta)
        max_states.push(max_list)
        if max_depth == dep:
            new_max_list = max_states.pop()
            max_val = evaluation(next_state, player)
            new_max_list = new_max_list[0], str(max_depth), str(max_val), str(alpha), str(beta)
            max_states.push(new_max_list)
            new_max_list = max_states.pop()
            new_max_list = ['-Infinity' if x == '-999999999' else x for x in new_max_list]
            new_max_list = ['Infinity' if x == '999999999' else x for x in new_max_list]
            max_states.push(new_max_list)
            p_max_list = max_states.pop()
            p_max_str = ",".join(map(str, p_max_list))
            max_states.push((p_max_list))
            O_file.write(p_max_str)
            O_file.write("\n")

            value = max(value, Min_Val(next_state, alpha, beta, depth + 1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
            new_min_list = min_states.pop()
            new_min_list = new_min_list[0], str(depth), str(value), str(alpha), str(beta)
            min_states.push(new_min_list)
            new_min_list = min_states.pop()
            new_min_list = ['Infinity' if x == '999999999' else x for x in new_min_list]
            min_states.push(new_min_list)
            p_min_list = min_states.pop()
            p_min_str = ",".join(map(str, p_min_list))
            min_states.push((p_min_list))
            O_file.write(p_min_str)
            O_file.write("\n")
            max_states.pop()
            continue
        new_max_list = max_states.pop()
        new_max_list = ['-Infinity' if x == '-999999999' else x for x in new_max_list]
        new_max_list = ['Infinity' if x == '999999999' else x for x in new_max_list]
        max_states.push(new_max_list)
        p_max_list = max_states.pop()
        p_max_str = ",".join(map(str, p_max_list))
        max_states.push((p_max_list))
        O_file.write(p_max_str)
        O_file.write("\n")
        value = max(value, Min_Val(next_state, alpha, beta, depth+1))
        if value >= beta:
            return value
        alpha = max(alpha, value)
        new_min_list = min_states.pop()
        min_states.push(new_min_list)
        new_max_list = max_states.pop()
        new_max_list = new_max_list[0],new_max_list[1],new_min_list[2],new_max_list[3],new_max_list[4]
        new_max_list = ['-Infinity' if x == '-999999999' else x for x in new_max_list]
        new_max_list = ['Infinity' if x == '999999999' else x for x in new_max_list]
        best_val_list[s,a] = int(new_min_list[2])
        max_states.push(new_max_list)
        p_max_list = max_states.pop()
        p_max_str = ",".join(map(str, p_max_list))
        max_states.push((p_max_list))
        O_file.write(p_max_str)
        O_file.write("\n")
        if alpha != neg_infinity:
            max_states.push(('root',str(depth),str(value), str(alpha), str(beta)))
            new_max_list = max_states.pop()
            new_max_list = ['-Infinity' if x == '-999999999' else x for x in new_max_list]
            new_max_list = ['Infinity' if x == '999999999' else x for x in new_max_list]
            max_states.push(new_max_list)
            p_max_list = max_states.pop()
            p_max_str = ",".join(map(str, p_max_list))
            max_states.push((p_max_list))
            O_file.write(p_max_str)
            O_file.write("\n")
    return value


def Min_Val(state, alpha, beta, depth):
    opponent = player_opponent(player)
    if cutoff_Test(depth):
        return evaluation(state, player)

    value = infinity
    available_moves = getValidMoves(state, opponent)
    new_max_list = max_states.pop()
    new_max_node = new_max_list[0]
    max_states.push(new_max_list)
    if len(available_moves) == 0 and new_max_node == 'pass':
        min_depth = depth + 1
        min_val = neg_infinity
        min_states.push(('pass',str(min_depth),str(min_val),str(alpha),str(beta)))
        new_min_list = min_states.pop()
        new_min_list = ['-Infinity' if x == '-999999999' else x for x in new_min_list]
        new_min_list = ['Infinity' if x == '999999999' else x for x in new_min_list]
        value = evaluation(state,player)
        new_min_list[2] = str(value)
        min_states.push(new_min_list)
        beta = min(value,beta)
        return beta
    elif len(available_moves) == 0:
        min_depth = depth+1
        min_val = neg_infinity
        min_states.push(('pass', str(min_depth), str(min_val), str(alpha), str(beta)))
        new_min_list = min_states.pop()
        new_min_list = ['-Infinity' if x == '-999999999' else x for x in new_min_list]
        new_min_list = ['Infinity' if x == '999999999' else x for x in new_min_list]
        min_states.push(new_min_list)
        p_min_list = min_states.pop()
        p_min_str = ",".join(map(str, p_min_list))
        min_states.push((p_min_list))
        O_file.write(p_min_str)
        O_file.write("\n")
        value = min(value,Max_Val(state,alpha,beta,depth+1))
        if value <= alpha:
            return value
        beta = min(beta, value)
        new_min_list = min_states.pop()
        new_min_list = ['-Infinity' if x == '-999999999' else x for x in new_min_list]
        new_min_list = ['Infinity' if x == '999999999' else x for x in new_min_list]
        new_min_list = new_min_list[0], str(min_depth), str(value), str(alpha), str(beta)
        min_states.push(new_min_list)
        new_max_list = max_states.pop()
        new_max_list = ['-Infinity' if x == '-999999999' else x for x in new_max_list]
        new_max_list = ['Infinity' if x == '999999999' else x for x in new_max_list]
        new_max_list = new_max_list[0], str(depth), str(value), str(alpha), str(beta)
        max_states.push(new_max_list)
        return value


    for (a, s) in available_moves:

        next_state = get_updated_state(a, s, copy.deepcopy(state), opponent)
        min_node = Dict[s]+str(a+1)
        min_depth = depth + 1
        min_val = neg_infinity
        min_list = min_node,str(min_depth),str(min_val),str(alpha),str(beta)
        min_states.push(min_list)
        new_min_list = min_states.pop()
        new_min_list = ['-Infinity' if x == '-999999999' else x for x in new_min_list]
        new_min_list = ['Infinity' if x == '999999999' else x for x in new_min_list]
        min_states.push(new_min_list)
        p_min_list = min_states.pop()
        p_min_str = ",".join(map(str, p_min_list))
        min_states.push((p_min_list))
        O_file.write(p_min_str)
        O_file.write("\n")
        value = min(value, Max_Val(next_state, alpha, beta, depth+1))
        if min_depth == dep:
            new_min_list = min_states.pop()
            min_val = evaluation(next_state,player)
            new_min_list = new_min_list[0], str(min_depth), str(min_val), str(alpha), str(beta)
            min_states.push(new_min_list)
            new_min_list = min_states.pop()
            new_min_list = ['-Infinity' if x == '-999999999' else x for x in new_min_list]
            new_min_list = ['Infinity' if x == '999999999' else x for x in new_min_list]
            min_states.push(new_min_list)
            new_max_list = max_states.pop()
            beta = min(min_val,beta)
            new_max_list = new_max_list[0], str(depth), str(min_val), str(alpha), str(beta)
            max_states.push(new_max_list)
            new_max_list = max_states.pop()
            new_max_list = ['-Infinity' if x == '-999999999' else x for x in new_max_list]
            new_max_list = ['Infinity' if x == '999999999' else x for x in new_max_list]
            max_states.push(new_max_list)
            p_min_list = min_states.pop()
            p_min_str = ",".join(map(str, p_min_list))
            min_states.push((p_min_list))
            O_file.write(p_min_str)
            O_file.write("\n")
        if value <= alpha:
            return value
        beta = min(beta, value)
        new_max_list = max_states.pop()
        new_max_val = new_max_list[2]
        max_states.push(new_max_list)
        new_min_list = min_states.pop()
        if new_min_list[4] != 'Infinity':
            new_min_list = new_min_list[0], new_min_list[1], str(new_max_val), str(new_min_list[3]), str(beta)
            new_min_list = ['-Infinity' if x == '-999999999' else x for x in new_min_list]
            new_min_list = ['Infinity' if x == '999999999' else x for x in new_min_list]
            min_states.push(new_min_list)
            p_min_list = min_states.pop()
            p_min_str = ",".join(map(str, p_min_list))
            min_states.push((p_min_list))
            O_file.write(p_min_str)
            O_file.write("\n")
        new_max_list = max_states.pop()
        new_max_list = 'pass',str(depth),str(value),str(alpha),str(beta)
        max_states.push(new_max_list)
        new_max_list = max_states.pop()
        new_max_list = ['-Infinity' if x == '-999999999' else x for x in new_max_list]
        new_max_list = ['Infinity' if x == '999999999' else x for x in new_max_list]
        max_states.push(new_max_list)
        p_max_list = max_states.pop()
        p_max_str = ",".join(map(str, p_max_list))
        max_states.push((p_max_list))
        O_file.write(p_max_str)
        O_file.write("\n")
    return value


def get_updated_state(x, y, state, player):
    global flips
    flips = checkValidMove(state, player, x, y)
    state[x][y] = player
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
            if not isValidSquare(x_step, y_step):
                continue
            while state[x_step][y_step] == opponent:
                x_step += x
                y_step += y
                if not isValidSquare(x_step, y_step):
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

    global dep, player, opponent
    player = contents[0]
    depth = int(contents[1])
    dep = depth



    opponent = player_opponent(player)

    arr = []
    for i in range(2, len(contents)):
        arr.append(list(contents[i]))

    if dep < 0:
        for i in range(8):
            st_list = arr[i]
            st_str = "".join(map(str, st_list))
            O_file.write(st_str)
            O_file.write("\n")

        O_file.write('Node,Depth,Value,Alpha,Beta')
        O_file.write("\n")
        max_states.push(['root', str(depth), '-Infinity', '-Infinity', 'Infinity'])
        p_max_list = max_states.pop()
        p_max_str = ",".join(map(str, p_max_list))
        max_states.push((p_max_list))
        O_file.write(p_max_str)
        O_file.write("\n")
    else:
        alpha_beta_search(arr,0,player)
        O_file.close()


main()
