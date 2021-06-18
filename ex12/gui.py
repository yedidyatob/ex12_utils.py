import tkinter as tk
from functools import partial
from boggle_board_randomizer import randomize_board

START_MSG = "Welcome to the Boggle game! Here you need to find as many words as " \
            "possible in three minutes. Are you ready to start?"


def readfile(file):
    words = []
    f_words = open(file)
    for line in f_words:
        word = line.strip()
        if word.isalpha():
            words.append(line.strip())
    f_words.close()
    return words


class GUI:
    CELLS_IN_ROW = 4
    TOTAL_CELLS = 16

    def __init__(self, root):
        self._root = root
        self.word = ""
        self.buttons = dict()
        self.board = randomize_board()
        self.score = 0
        self.guessed_words = []
        root.geometry("600x700")
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.rowconfigure(root, 1, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)
        self.create_text_frame()
        self.create_desk_frame()

    def create_text_frame(self):
        self.text_frame = tk.Frame(root, background="LightBlue1")
        self.text_frame.grid(row=0, column=0, sticky="snew")
        self._create_menu(self.text_frame)

    def create_desk_frame(self):
        self.desk_frame = tk.Frame(root, bd=20, background="LightBlue1")
        self.desk_frame.grid(row=1, column=0, sticky="snew")
        self._create_grid(self.desk_frame)

    def _create_grid(self, frame):
        for i in range(self.CELLS_IN_ROW):
            tk.Grid.rowconfigure(frame, i, weight=1)
            for j in range(self.CELLS_IN_ROW):
                tk.Grid.columnconfigure(frame, j, weight=1)
                button = tk.Button(frame, text=self.board[i][j],
                                   width=6, height=3, command=partial(self.button_action, i, j),
                                   font=("Comic Sans MS", 15, "bold"), relief=tk.GROOVE,
                                   background='mint cream', activebackground="LightBlue1", fg="blue4")
                button.bind("<Button-3>", lambda event: self.undo_action(i, j))
                button.grid(row=i, column=j, sticky="snew")
                self.buttons[(i, j)] = button

    def button_action(self, row, col):
        self.buttons[(row, col)].configure(background="PaleGreen1")
        self.word += self.buttons[(row, col)]["text"]
        self.word_label["text"] = self.word

    def undo_action(self, row, col):
        self.buttons[(row, col)].configure(background="light cyan")
        self.word.replace(self.buttons[(row, col)]["text"], "")

    def countdown(self):
        pass

    def update_score(self):
        self.score += int(len(self.word)) * 2
        self.score_value["text"] = str(self.score)

    def check_word(self):
        words_list = readfile("boggle_dict.txt")
        if self.word in words_list:
            if self.word not in self.guessed_words:
                self.guessed_words.append(self.word)
                self.update_score()
        self.word = ""
        self.word_label["text"] = self.word
        for (i, j) in self.buttons.keys():
            self.buttons[(i, j)].configure(background="light cyan")

    def refresh_board(self):
        self.desk_frame.destroy()
        self.create_desk_frame()

    def _create_menu(self, frame):
        tk.Grid.rowconfigure(frame, 0, weight=1)
        tk.Grid.rowconfigure(frame, 1, weight=1)
        tk.Grid.rowconfigure(frame, 2, weight=1)
        tk.Grid.columnconfigure(frame, 0, weight=1)
        tk.Grid.columnconfigure(frame, 1, weight=1)
        tk.Grid.columnconfigure(frame, 2, weight=1)

        game_name = tk.Label(frame, text="Find all the words!",
                             background="LightBlue1", fg="blue4", font=("Snap ITC", 20))
        self.word_label = tk.Label(frame, background="LightBlue1",
                                   fg="blue4", font=("Comic Sans MS", 12))
        score_label = tk.Label(frame, text="SCORE:", background="LightBlue1", fg="blue4", font=("Comic Sans MS", 12))
        self.score_value = tk.Label(frame, background="LightBlue1", fg="blue4", font=("Comic Sans MS", 12))
        time_label = tk.Label(frame, background="LightBlue1", bitmap="hourglass", fg="blue4")
        check_word = tk.Button(frame, text='CHECK', background="LightBlue1",
                               activebackground="PaleGreen1", command=self.check_word,
                               fg="blue4", font=("Comic Sans MS", 10, "bold"))
        refresh = tk.Button(frame, text='REFRESH', background="LightBlue1",
                            activebackground="PaleGreen1", command=self.refresh_board,
                            fg="blue4", font=("Comic Sans MS", 10, "bold"))
        # self.timer = tk.Label(frame, background="LightBlue1", font=("Franklin Gothic Medium", 10))

        game_name.grid(row=0, column=1)
        score_label.grid(row=1, column=2)
        self.score_value.grid(row=1, column=3)
        time_label.grid(row=1, column=0)
        # self.timer.grid(row=1, column=3)
        self.word_label.grid(row=1, column=1)
        check_word.grid(row=2, column=0)
        refresh.grid(row=2, column=2)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    root.wm_title("BOGGLE")
    GUI(root)
    root.mainloop()