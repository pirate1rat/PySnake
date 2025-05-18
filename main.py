import sys
import importlib
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config import *
import solutions
import game

class GUI:
    def __init__(self, my_game: game.Game):
        self.main_window = self.set_main_window()

        self.game_frame = tk.Frame()
        self.game_frame.pack(side="left")
        self.stat_frame = tk.Frame()
        self.stat_frame.pack(side="right")
        self.snake_canv = self.set_game_canvas(self.game_frame)
        self.stats_canv = self.set_stats_canvas(self.stat_frame)

        self.set_game_buttons(self.game_frame)

        self.my_game = my_game
        self.squares = []
        self.module = None

        self.main_window.after(GAME_SPEED, self.update_game)
        self.main_window.mainloop()

    def set_main_window(self):
        main_window = tk.Tk()
        main_window.geometry("1000x700")
        main_window.title("PySnake")
        main_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        return main_window
    def set_game_canvas(self, frame):
        game_canvas = tk.Canvas(frame, bg = "black", height=HEIGHT*BLOCK_SIZE, width=WIDTH*BLOCK_SIZE)
        game_canvas.grid(row=1, column=0)
        game_canvas.pack(padx=30, pady=30)
        return game_canvas
    def set_game_buttons(self, frame):
        reg = get_registry()

        self._option_buttons = tk.Frame(frame)
        self._solution_var = tk.StringVar(self._option_buttons)
        self._solution_var.set(reg[0])
        self._solution_menu = tk.OptionMenu(self._option_buttons, self._solution_var, *reg)
        self._solution_menu.grid(row=1, column=1)
        self._solution_var.trace_add('write', self.import_solution)

        self._active_buttons = tk.Frame(frame)
        self._play = tk.PhotoImage(file="images/play.png")
        self._play_button = tk.Button(self._active_buttons, image=self._play, command= self.game_running)
        self._play_button.grid(row=0, column=0)
        self._pause = tk.PhotoImage(file="images/pause.png")
        self._pause_button = tk.Button(self._active_buttons, image=self._pause, command= self.game_paused)
        self._pause_button.grid(row=0, column=1)
        self._nothing = tk.Frame(self._active_buttons, width=64, height=64)
        self._nothing.grid(row=0, column=2)
        self._restart = tk.PhotoImage(file="images/restart.png")
        self._restart_button = tk.Button(self._active_buttons, image=self._restart, command= self.game_restart)
        self._restart_button.grid(row=0, column=3)

        self._option_buttons.pack()
        self._active_buttons.pack()
        self.import_solution()
    def set_stats_canvas(self, frame):
        self.fig, self.ax = plt.subplots()
        canvas = FigureCanvasTkAgg(self.fig, master=frame)
        canvas.get_tk_widget().pack()
        return canvas
    def on_closing(self):
        sys.exit()

    def game_running(self):
        self.my_game.resume()
    def game_paused(self):
        self.my_game.pause()
    def game_restart(self):
        self.my_game.restart()
        self.update_canv(self.snake_canv, self.squares, self.my_game.conv_to_rgb())

    def update_game(self):
        if self.my_game.GAME_RUNNING:
            print(self.module)
            self.my_game.update_game(self.module)
            self.update_canv(self.snake_canv, self.squares, self.my_game.conv_to_rgb())
        self.main_window.after(GAME_SPEED, self.update_game)

    def import_solution(self, *args):
        #print(self._solution_var.get())
        try:
            self.module = importlib.import_module(f"solutions.{self._solution_var.get()}")
        except ImportError as e:
            print(f"Nie udało się zaimportować {f"solutions.{self._solution_var.get()}"}", e)
        print(self.module)

    def update_canv(self, snake_canv, squares, board):
        for sq in squares:
            snake_canv.delete(sq)
        squares.clear()

        for x in range(WIDTH):
            for y in range(HEIGHT):
                #print(x, y)
                square = snake_canv.create_rectangle(x*BLOCK_SIZE + 1, y*BLOCK_SIZE + 1, 
                                                     (x+1)*BLOCK_SIZE + 1, (y+1)*BLOCK_SIZE + 1,
                                                    fill=("#%02x%02x%02x" % board[x][y]))
                squares.append(square)
            #print(board)
    
        #square = snake_canv.create_rectangle(0*BLOCK_SIZE, 0*BLOCK_SIZE, (0+1)*BLOCK_SIZE, (0+1)*BLOCK_SIZE, fill=("#%02x%02x%02x" % board[0][0]))
        #square = snake_canv.create_rectangle(1*BLOCK_SIZE, 0*BLOCK_SIZE, (1+1)*BLOCK_SIZE, (0+1)*BLOCK_SIZE, fill=("#%02x%02x%02x" % board[1][0]))
        self.snake_canv.update()

def main():
    snake = game.Game()
    root = GUI(snake)

if __name__ == "__main__":
    main()