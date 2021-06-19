from boggle_board_randomizer import LETTERS, randomize_board
from pprint import pprint
from time import time

SIZE = 4
PATHS = 1
WORDS = 2


def is_valid_path(board, path, words):
    """

    :param board:
    :param path:
    :param words:
    :return:
    """
    word = ""
    if path:
        for index, cell in enumerate(path):
            if index != 0:
                if not is_neighbor(cell, path[index-1]):
                    return  # check if path is continuous
            if cell in path[:index]:
                return  # check if cell appears twice
            if not is_legal_cell(cell, board):
                return
            word += board[cell[0]][cell[1]]
        if word in words:
            return True


def board_to_dict(board):  # NOT IN USE
    board_dict = {(i, j): board[i][j] for i in range(SIZE) for j in range(SIZE)}
    return board_dict


def is_legal_cell(cell, board):
    """

    :param board:
    :param cell:
    :return:
    """
    max_index = len(board) - 1
    for i in cell:
        if not 0 <= i <= max_index:
            return False
    return True


def get_content(cell, board):
    if is_legal_cell(cell, board):
        return board[cell[0]][cell[1]]


def is_neighbor(cell1, cell2):
    """
    ASSUMES CELLS ARE LEGAL! DOES NOT CHECK IF CELLS ARE VALID.
    checks if cells are neighbors (in 8 directions).
    :param cell1: tuple
    :param cell2: tuple
    :return: bool
    """

    for i in range(2):
        if abs(cell1[i] - cell2[i]) > 1:
            return False
    if cell2 != cell1:
        return True


def all_neighbors(cell):
    moves = [-1, 0, 1]
    neighbors = [(cell[0] + i, cell[1] + j) for i in moves for j in moves]
    neighbors.remove(cell)
    return neighbors


def helper_1(n, cell, paths, board, words, func, path=None):
    if not path:
        path = []
    new_path = path[:] + [cell]
    new_word = path_to_word(new_path, board)
    new_words = [word for word in words if word.startswith(new_word)]
    if new_words:
        for neighbor in all_neighbors(cell):
            if neighbor in new_path or not is_legal_cell(neighbor, board):
                continue
            else:
                last_added = len(get_content(cell, board))
                if (n == last_added and func == WORDS) \
                        or (n <= 1 and func == PATHS):
                    if new_path not in paths:
                        paths.append(new_path)
                else:
                    subtract = 1
                    if func == WORDS:
                        subtract = last_added
                    helper_1(n - subtract, neighbor, paths,
                             board, new_words, func, new_path)


def path_to_word(path, board):
    """

    :param path:
    :param board:
    :return:
    """
    return "".join(board[cell[0]][cell[1]] for cell in path)


def helper_2(n, board, words, func):
    paths = []
    for i in range(SIZE):
        for j in range(SIZE):
            cell = (i, j)
            helper_1(n, cell, paths, board, words, func)
    filtered = []
    for path in paths:
        word = "".join(board[cell[0]][cell[1]] for cell in path)
        if word in words:
            filtered.append(path)
    return filtered


def find_length_n_paths(n, board, words):
    return helper_2(n, board, words, PATHS)


def find_length_n_words(n, board, words):
    return helper_2(n, board, words, WORDS)



def max_score_paths(board, words):
    pass


if __name__ == '__main__':
    # bord = randomize_board(LETTERS)
    bord1 = [['O', 'RE', 'E', 'Y'],
             ['E', 'J', 'U', 'H'],
             ['H', 'E', 'N', 'O'],
             ['F', 'S', 'P', 'E']]
    pprint(bord1)
    start = time()
    milon = open("boggle_dict.txt")
    lines = set(line.strip() for line in milon.readlines())
    pat = [(1, 3), (2, 3), (3, 3)]
    # print(is_valid_path(bord1, pat, lines))
    pats = find_length_n_paths(3, bord1, lines)
    wrds = find_length_n_words(4, bord1, lines)
    pats1 = [pat for pat in pats if len(path_to_word(pat, bord1)) == 4]
    wrds1 = [wrd for wrd in wrds if "RE" in path_to_word(wrd, bord1)]
    print(len(pats1))
    print(len(wrds1))
    for pat in pats:
        print(path_to_word(pat, bord1))
    print("words:")
    for pat in wrds:
        print(path_to_word(pat, bord1))
    end = time()
    print(end-start)
    milon.close()

