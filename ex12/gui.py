import tkinter as tk
import time
from boggle_board_randomizer import randomize_board


class GUI:
    CELLS_IN_ROW = 4
    TOTAL_CELLS = 16

    def __init__(self, root):
        self._root = root
        root.geometry("400x500")
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.rowconfigure(root, 1, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)
        text_frame = tk.Frame(root, background="LightBlue1")
        desk_frame = tk.Frame(root, bd=20, background="LightBlue1")
        text_frame.grid(row=0, column=0, sticky="snew")
        desk_frame.grid(row=1, column=0, sticky="snew")
        self._create_grid(desk_frame)
        self._create_menu(text_frame)

    def _create_grid(self, frame):
        self.buttons = []
        board = randomize_board()
        for i in range(self.CELLS_IN_ROW):
            row = []
            tk.Grid.rowconfigure(frame, i, weight=1)
            for j in range(self.CELLS_IN_ROW):
                tk.Grid.columnconfigure(frame, j, weight=1)
                button = tk.Button(frame, text=board[i][j], width=6, height=3, background='light cyan')
                button.grid(row=i, column=j, sticky="snew")
            self.buttons.append(row)

    def countdown(self, count, label):
        if count > 0:
            label["text"] = count
            count -= 1
            root.after(1000, count, lambda: self.countdown(count, label))

    def _create_menu(self, frame):
        tk.Grid.rowconfigure(frame, 0, weight=1)
        tk.Grid.columnconfigure(frame, 0, weight=1)
        tk.Grid.columnconfigure(frame, 1, weight=1)
        tk.Grid.columnconfigure(frame, 2, weight=1)

        score = tk.Label(frame, text="Score:", background="white", font=("Helvetica", 20))
        timer = tk.Label(frame, text="Timer:", background="white", font=("Helvetica", 20))
        score.grid(row=0, column=0)
        timer.grid(row=0, column=1)
        time_label = tk.Label(frame, background="white", font=("Helvetica", 20))
        time_label.grid(row=0, column=2)
        self.countdown(180, time_label)




if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    root.wm_title("BOGGLE")
    GUI(root)
    root.mainloop()
