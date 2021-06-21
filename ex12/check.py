import tkinter as tk
from functools import partial
from boggle_board_randomizer import randomize_board


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

    def __init__(self, root):
        self.word = ""
        self.word_dict = dict()
        self.buttons = dict()
        self.board = randomize_board()
        self.score = 0
        self.time_limit = 180
        self.guessed_words = []
        self._root = root
        self._root.geometry("600x750")
        tk.Grid.rowconfigure(self._root, 0, weight=1)
        tk.Grid.rowconfigure(self._root, 1, weight=1)
        tk.Grid.columnconfigure(self._root, 0, weight=1)
        self.text_frame = tk.Frame(self._root, height=150, width=600, background="LightBlue1")
        self.text_frame.grid(row=0, column=0, sticky="snew")
        self._create_menu(self.text_frame)
        self.desk_frame = tk.Frame(self._root, height=600, width=600, bd=20, background="LightBlue1")
        self.desk_frame.grid(row=1, column=0, sticky="snew")
        self._create_grid(self.desk_frame)
        self.countdown(self.time_limit)

    def _create_grid(self, frame):
        for i in range(self.CELLS_IN_ROW):
            tk.Grid.rowconfigure(frame, i, weight=1)
            for j in range(self.CELLS_IN_ROW):
                tk.Grid.columnconfigure(frame, j, weight=1)
                button = tk.Button(frame, text=self.board[i][j],
                                   width=6, height=3, command=partial(self.button_action, i, j),
                                   font=("Comic Sans MS", 15, "bold"), relief=tk.GROOVE,
                                   background='mint cream', activebackground="LightBlue1", fg="blue4")
                button.grid(row=i, column=j, sticky="snew")
                self.buttons[(i, j)] = button
        for coordinates, button in self.buttons.items():
            button.bind("<Double-1>", lambda event: self.undo_action(coordinates[0], coordinates[1]))

    def button_action(self, row, col):
        self.buttons[(row, col)].configure(background="PaleGreen1")
        if (row, col) not in self.word_dict.keys():
            self.word_dict[(row, col)] = self.buttons[(row, col)]["text"]
            self.word += self.buttons[(row, col)]["text"]
        self.word_label["text"] = self.word

    def undo_action(self, row, col):
        self.buttons[(row, col)].configure(background="mint cream")
        self.word.replace(self.buttons[(row, col)]["text"], "")

    def update_score(self):
        self.score += int(len(self.word)) * 2
        self.score_value["text"] = str(self.score)

    def check_word(self):
        words_list = readfile("boggle_dict.txt")
        if self.word in words_list:
            if self.word not in self.guessed_words:
                self.guessed_words.append(self.word)
                self.update_score()
        self.word_dict.clear()
        self.word = ""
        self.word_label["text"] = self.word
        for (i, j) in self.buttons.keys():
            self.buttons[(i, j)].configure(background="light cyan")

    def refresh_board(self):
        # self.desk_frame.destroy()
        # self.create_desk_frame()
        pass

    def countdown(self, count):
        if len(str(count % 60)) == 1:
            self.timer["text"] = str(count // 60) + ":" + "0" + str(count % 60)
        else:
            self.timer["text"] = str(count // 60) + ":" + str(count % 60)
        if count > 0:
            self._root.after(1000, self.countdown, count - 1)

    def _create_menu(self, frame):
        tk.Grid.rowconfigure(frame, 0, weight=3)
        tk.Grid.rowconfigure(frame, 1, weight=1)
        tk.Grid.rowconfigure(frame, 2, weight=2)
        tk.Grid.rowconfigure(frame, 3, weight=1)
        tk.Grid.columnconfigure(frame, 0, weight=1)
        tk.Grid.columnconfigure(frame, 1, weight=1)
        tk.Grid.columnconfigure(frame, 2, weight=1)
        tk.Grid.columnconfigure(frame, 3, weight=1)
        tk.Grid.columnconfigure(frame, 4, weight=1)

        game_name = tk.Label(frame, text="Find all the words!",
                             background="LightBlue1", fg="blue4", font=("Snap ITC", 20))
        self.word_label = tk.Label(frame, background="LightBlue1",
                                   fg="blue4", font=("Comic Sans MS", 12))
        score_label = tk.Label(frame, text="SCORE:", background="LightBlue1", fg="blue4", font=("Comic Sans MS", 12))
        self.score_value = tk.Label(frame, text="0", background="LightBlue1", fg="blue4", font=("Comic Sans MS", 12))
        time_label = tk.Label(frame, background="LightBlue1", bitmap="hourglass", fg="blue4")
        check_word = tk.Button(frame, text='CHECK', background="LightBlue1",
                               activebackground="PaleGreen1", command=self.check_word,
                               fg="blue4", font=("Comic Sans MS", 10, "bold"))
        refresh = tk.Button(frame, text='REFRESH', background="LightBlue1",
                            activebackground="PaleGreen1", command=self.refresh_board,
                            fg="blue4", font=("Comic Sans MS", 10, "bold"))
        self.timer = tk.Label(frame, background="LightBlue1", fg="blue4", font=("Comic Sans MS", 12))

        game_name.grid(row=0, column=2)
        time_label.grid(row=1, column=0)
        self.timer.grid(row=1, column=1)
        score_label.grid(row=1, column=3)
        self.score_value.grid(row=1, column=4)
        self.word_label.grid(row=2, column=2)
        check_word.grid(row=3, column=1)
        refresh.grid(row=3, column=3)


class Game:
    def __init__(self, root):
        self.root = root
        root.geometry("400x500")
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="snew")
        self.create_window()

    def create_window(self):
        tk.Grid.rowconfigure(self.main_frame, 0, weight=1)
        tk.Grid.rowconfigure(self.main_frame, 1, weight=1)
        tk.Grid.rowconfigure(self.main_frame, 2, weight=1)
        tk.Grid.columnconfigure(self.main_frame, 0, weight=1)

        self.name_label = tk.Frame(self.main_frame, bd=20, background="LightBlue1")
        self.name_label.grid(row=0, column=0, sticky="snew")
        name = tk.Label(self.name_label, text="WELCOME\n TO\n BOGGLE!!!",
                        background="LightBlue1", fg="blue4", font=("Snap ITC", 20))
        name.place(x=65, y=30)

        self.start_label = tk.Frame(self.main_frame, bd=20, background="LightBlue1")
        self.start_label.grid(row=1, column=0, sticky="snew")
        start_button = tk.Button(self.start_label, text='START GAME', background="LightBlue1",
                                 activebackground="PaleGreen1", command=self.start_game,
                                 fg="blue4", font=("Comic Sans MS", 15, "bold"))
        start_button.place(x=100, y=50)

        self.exit_label = tk.Frame(self.main_frame, bd=20, background="LightBlue1")
        self.exit_label.grid(row=2, column=0, sticky="snew")
        exit_button = tk.Button(self.exit_label, text='EXIT', background="LightBlue1",
                                activebackground="tomato", command=lambda: self.root.destroy(),
                                fg="blue4", font=("Comic Sans MS", 15, "bold"))
        exit_button.place(x=135, y=50)

    def start_game(self):
        self.main_frame.destroy()
        GUI(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("BOGGLE")
    Game(root)
    root.mainloop()
