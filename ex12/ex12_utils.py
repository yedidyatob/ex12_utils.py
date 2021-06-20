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
                if not is_neighbor(cell, path[index - 1]):
                    return  # check if path is continuous
            if cell in path[:index]:
                return  # check if cell appears twice
            if not is_legal_cell(cell, board):
                return
            word += board[cell[0]][cell[1]]
        if word in words:
            return word


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
    length = len(new_word)
    new_words = {word: 0 for word in words if new_word in word[:length]}
    if new_words:
        last_added = len(get_content(cell, board))
        if (n == last_added and func == WORDS) \
                or (n <= 1 and func == PATHS):
            if new_path not in paths:
                paths.append(new_path)
        else:
            for neighbor in all_neighbors(cell):
                if neighbor in new_path or not is_legal_cell(neighbor, board):
                    continue
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
    all_paths = {}
    longest = len(max(words, key=len))
    for i in range(1, longest):
        new_paths = {path_to_word(path, board): path for path in
                     find_length_n_paths(i, board, words)}
        for word in new_paths:
            if word in all_paths:
                if len(new_paths[word]) > len(all_paths[word]):
                    all_paths[word] = new_paths[word]
            else:
                all_paths[word] = new_paths[word]
    return list(all_paths.items())  # change to VALUES!!!!


if __name__ == '__main__':
    bord = randomize_board(LETTERS)
    bord1 = [['D', 'C', 'B', 'A'],
             ['G', 'A', 'D', 'E'],
             ['T', 'J', 'Y', 'T'],
             ['N', 'M', 'F', 'I']]

    milon = open("boggle_dict.txt")
    lines = milon.readlines()
    lines_dic = {line[:-1]: 0 for line in lines}
    start = time()
    all_paths = []
    pprint(bord)
    print(max_score_paths(bord, lines_dic))
    # find_length_n_paths(10, bord1, lines_dic)
    end = time()
    print(end - start)
