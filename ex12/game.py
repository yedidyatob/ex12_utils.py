###############################################
# FILE: game.py
# EXERCISE: intro2cs2 ex12 2021
# DESCRIPTION: Boggle game runner
###############################################


import tkinter as tk
import gui


if __name__ == "__main__":
    root = tk.Tk()
    # implement the name of the window
    root.wm_title("BOGGLE")
    # call to the start menu
    gui.StartGame(root)
    # run the mainloop
    root.mainloop()
