import copy
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

Dict = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
neg_infinity = -999999999
infinity = 999999999
#alpha = neg_infinity
#beta = infinity

move_directions = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

nodes = []
max_nodes =[]
new_state =[]
class Reversi:

    def __init__(self,state,alpha,beta,depth):
        self.alpha = alpha
        self.beta = beta
        self.depth = depth
        self.state = state
        self.value = 0


    def alpha_beta_search(self,state,player,alpha,beta,maximize,max_depth):
        alpha = 10
        beta =20
        nxtNode = Reversi(self.state,alpha,beta,max_depth+1)
        print nxtNode.state
        print nxtNode.alpha
        print nxtNode.beta
        print nxtNode.depth
        alpha = 40
        beta = 50
        nxtNode1 = Reversi(self.state,alpha,beta,max_depth+1)
        next_state = state
        new_state = nxtNode1.get_updated_state(2,3,next_state,player)

        nxtNode1.state = new_state

        print nxtNode1.state
        print nxtNode1.alpha
        print nxtNode1.beta
        print nxtNode1.depth
        self.depth = max_depth
        if self.depth > depth:
            return self.evaluation(state,player)
        if maximize == True:
            value = neg_infinity
            available_moves = self.getValidMoves(state, player)
            for (a,s) in available_moves:
                next_state = state





    def player_opponent(self,player):
        if player == 'X':
            opponent = 'O'
        else:
            if player == 'O':
                opponent = 'X'
        return opponent

    def isValidSquare(self,i, j):
        if 0 <= i <= 7 and 0 <= j <= 7:
            return True
        else:
            return False

    def getValidMoves(self,state, player):
        valid_moves = []

        for i in range(8):
            for j in range(8):
                if self.checkValidMove(state, player, i, j):
                    valid_moves.append([i, j])
        return valid_moves

    def checkValidMove(self,state, player, i, j):
        if self.state[i][j] != '*' or not self.isValidSquare(i, j):
            return False

        self.state[i][j] = player

        opponent = self.player_opponent(player)

        valid_flips = []

        for x, y in move_directions:

            x_step = i
            y_step = j

            x_step = x_step + x
            y_step = y_step + y

            if self.isValidSquare(x_step, y_step) and self.state[x_step][y_step] == opponent:
                x_step += x
                y_step += y

                while self.state[x_step][y_step] == opponent:
                    x_step += x
                    y_step += y

                if self.state[x_step][y_step] == player:
                    while True:
                        x_step -= x
                        y_step -= y
                        if x_step == i and y_step == j:
                            break
                        valid_flips.append([x_step, y_step])

        self.state[i][j] = '*'
        if not len(valid_flips) == 0:
            return valid_flips
        return False

    def evaluation(self, state, player):
        X_Sum = 0
        O_Sum = 0
        for i in range(0, 7):
            for j in range(0, 7):
                if self.state[i][j] == 'X':
                    X_Sum = X_Sum + weighted_arr[i][j]

                else:
                    if self.state[i][j] == 'O':
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

    def get_updated_state(self,x, y, state, player):
        global flips
        flips = self.checkValidMove(state, player, x, y)
        self.state[x][y] = player
        # print flips
        if flips == False:
            return state

        for i, j in flips:
            self.state[i][j] = player
        return state

if __name__ == '__main__':
    file = open('input.txt', 'r')

    contents = contents = file.read().splitlines()
    global player, depth
    player = contents[0]
    depth = int(contents[1])

    arr = []
    for i in range(2, len(contents)):
        arr.append(list(contents[i]))

    root = Reversi(arr,neg_infinity,infinity,0)
    root.alpha_beta_search(arr,player,neg_infinity,infinity,True,0)



