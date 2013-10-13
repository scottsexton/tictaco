import random


class Grid(object):
    def __init__(self, progress = ''):
        if progress != '':
            previous_moves = list(progress)
            self.squares = [None]*9
            for position in xrange(9):
                if previous_moves[position] != 'X' and previous_moves[position] != 'O':
                    previous_moves[position] = '&nbsp;'
                self.squares[position] = previous_moves[position]
        else:
            self.squares = ['&nbsp;']*9

    def get_board(self):
        board_html = "<table border='0' cellspacing='0' cellpadding='0'>"
        for position in xrange(9):
            if position in (0, 3, 6):
                board_html += "<tr>"
            if self.squares[position] == '&nbsp;':
                board_html += "<td class='box{0}' id='box{0}' onClick='callSomePython({0})' title='Click to play this square.'>{1}</td>".format(position+1, self.squares[position])
            else:
                board_html += "<td class='box{0}'>{1}</td>".format(position+1, self.squares[position])
            if position in (2, 5, 8):
                board_html += "</tr>"
        board_html += "</table>"
        board_html += "<input type='hidden' name='pg' id='pg' value='{0}'>".format(''.join(self.squares))
        return board_html

    def make_move(self, position, letter):
        self.squares[int(position)] = letter

    def undo_move(self, position):
        self.squares[position] = '&nbsp;'

    def check_winner(self):
        winning_combos = [[0,1,2],[3,4,5],[6,7,8],
                          [0,3,6],[1,4,7],[2,5,8],
                          [0,4,8],[2,4,6]]
        for combo in winning_combos:
            if self.squares[combo[0]] != '&nbsp;' and (self.squares[combo[0]] == self.squares[combo[1]] == self.squares[combo[2]]):
                return self.squares[combo[0]]

    def get_empty_squares(self):
        return [position for position in range(9) if self.squares[position] == '&nbsp;']

    def game_state(self):
        winner = self.check_winner()
        if winner:
            return winner
        elif not self.get_empty_squares():
            return "draw"
        else:
            return "in progress"

# Module level functions
def minimax_eval(grid, position, computer_letter, eval_letter):
    try:
        grid.make_move(position, eval_letter)
        state = grid.game_state()
        human_letter = ('X','O')[computer_letter == 'X']
        if state == 'draw':
            return 0
        elif state == computer_letter:
            return 1
        elif state == human_letter:
            return -1
        other_letter = ('X','O')[eval_letter == 'X']
        game_results = (minimax_eval(grid, next_move, computer_letter, other_letter) for next_move in grid.get_empty_squares())

        if eval_letter == computer_letter:
            min_element = 1
            for result in game_results:
                if result == -1:
                    return result
                min_element = min(result, min_element)
            return min_element
        else:
            max_element = -1
            for result in game_results:
                if result == 1:
                    return result
                max_element = max(result, max_element)
            return max_element
    finally:
        grid.undo_move(position)

def computer_move(grid, computer_letter):
    possibilities = grid.get_empty_squares()
    evaluated_moves = []
    for possible in possibilities:
        evaluated_moves.append((possible, minimax_eval(grid, possible, computer_letter, computer_letter)))
    random.shuffle(evaluated_moves)
    evaluated_moves.sort(key = lambda (possible, winner): winner)
    grid.make_move(evaluated_moves[-1][0], computer_letter)

def human_move(grid, human_letter, position):
    grid.make_move(position, human_letter)

def pretty_message(state):
    if state == "draw":
        return "<p>It's a draw. <a href='.'>Rematch!</a></p>"
    return "<p>"+state+" has won the game! <a href='.'>Rematch!</a></p>"

def next_turn(human_letter, position, progress):
    g = Grid(progress)
    human_move(g, human_letter, position)
    state = g.game_state()
    if state != "in progress":
        return pretty_message(state) + g.get_board()
    computer_letter = ('X', 'O')[human_letter == 'X']
    computer_move(g, computer_letter)
    state = g.game_state()
    if state != "in progress":
        return pretty_message(state) + g.get_board()
    return g.get_board()

def begin_game(human_letter):
    g = Grid()
    computer_letter = ('X', 'O')[human_letter == 'X']
    if computer_letter == 'X':
        computer_move(g, computer_letter)
    return g.get_board()
