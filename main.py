import sys
import importlib
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

from config import *
import solutions
import game_logic.game as game

class Chart:
    def __init__(self, frame, color):
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack()
        self.color = color

class GUI:
    def __init__(self, my_game: game.Game):
        self.VISIBLE = True
        self.my_game = my_game
        self.squares = list()
        self.module = None
        self.data = {"points" : [],
                     "turns" : [],
                     "times": []}
        self.games = list()

        self.main_window = self.set_main_window()

        self.upframe = tk.Frame()
        self.upframe.pack()
        self.game_frame = tk.Frame(self.upframe)
        self.game_frame.pack(side="left")
        self.stat_frame = tk.Frame(self.upframe)
        self.stat_frame.pack(side="right")
        self.console_frame = tk.Frame()
        self.console_frame.pack()

        self.snake_canv = self.set_game_canvas(self.game_frame)
        self.stat_cv1 = Chart(self.stat_frame, "black")
        self.stat_cv2 = Chart(self.stat_frame, "blue")
        #self.stat_cv3 = Chart(self.stat_frame, "green")
        self.set_console(self.console_frame)

        self.set_game_buttons(self.game_frame)
        self.set_stat_buttons(self.stat_frame)
        

        self.main_window.after(GAME_SPEED, self.update_game)
        self.main_window.mainloop()

    def set_main_window(self):
        main_window = tk.Tk()
        main_window.geometry("1050x950")
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
        self._solution_menu.pack()
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
        self._loop = tk.PhotoImage(file="images/loop.png")
        self._loop_button = tk.Button(self._active_buttons, image=self._loop, command= self.game_in_loop)
        self._loop_button.grid(row=1, column=0)
        self._visible = tk.PhotoImage(file="images/visible.png")
        self._visible_button = tk.Button(self._active_buttons, image=self._visible, command= self.game_visible)
        self._visible_button.grid(row=1, column=1)

        self._option_buttons.pack()
        self._active_buttons.pack()
        self.import_solution()
    def set_stat_buttons(self, frame):
        self.keys = list()
        for key in self.data.keys():
            self.keys.append(key)
        
        self._select_charts = tk.Frame(frame)
        self._chart1_var = tk.StringVar(self._select_charts)
        self._chart1_var.set(self.keys[0])
        self._chart1_menu = tk.OptionMenu(self._select_charts, self._chart1_var, *self.keys)
        self._chart1_menu.grid(row=0, column=0)
        self._chart1_var.trace_add('write', lambda *args: self.update_chart(self.stat_cv1, self.games, self.data[self._chart1_var.get()]))
        self._chart2_var = tk.StringVar(self._select_charts)
        self._chart2_var.set(self.keys[1])
        self._chart2_menu = tk.OptionMenu(self._select_charts, self._chart2_var, *self.keys)
        self._chart2_menu.grid(row=0, column=1)
        self._chart2_var.trace_add('write', lambda*args: self.update_chart(self.stat_cv2, self.games, self.data[self._chart1_var.get()]))

        self._chart_buttons = tk.Frame(frame)
        self._clear_chart = tk.Button(master=self._chart_buttons, text="clear data", command=self.clear_data)
        self._clear_chart.grid(row=0, column=0)
        self._save_data = tk.Button(master=self._chart_buttons, text="save data", command=self.save_data)
        self._save_data.grid(row=0, column=1)

        self._select_charts.pack()
        self._chart_buttons.pack()
    def set_console(self, frame):
        self._last_games = tk.Text(frame, height=11, width=80)
        self._last_games.config(state=tk.DISABLED)
        self._last_games.pack()
        self._averages = tk.Text(frame, height=6, width=40)
        self._averages.config(state=tk.DISABLED)
        self._averages.pack()

    def on_closing(self):
        sys.exit()
    def game_running(self):
        self.my_game.resume()
    def game_paused(self):
        self.my_game.pause()
    def game_restart(self):
        self.my_game.restart()
        self.update_canv(self.snake_canv, self.squares, self.my_game.conv_to_rgb())
    def game_in_loop(self):
        self.my_game.in_loop()
    def game_visible(self):
        self.VISIBLE = not self.VISIBLE

    def update_game(self):
        if self.my_game.GAME_RUNNING:
            parameters = self.my_game.update_game(self.module)
            if self.VISIBLE:
                self.update_canv(self.snake_canv, self.squares, self.my_game.conv_to_rgb())
            if parameters:
                self.statistics(parameters)

        self.main_window.after(GAME_SPEED, self.update_game)

    def import_solution(self, *args):
        #print(self._solution_var.get())
        try:
            self.module = importlib.import_module(f"solutions.{self._solution_var.get()}")
        except ImportError as e:
            print(f"Nie udało się zaimportować {f"solutions.{self._solution_var.get()}"}", e)

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

    def update_chart(self, chr: Chart, datax, datay):
        chr.ax.clear()
        chr.ax.plot(datax, datay, color=chr.color)
        if datay:
            mean = np.mean(datay)
            chr.ax.axhline(mean, color='red', linestyle='--', label=f'average = {mean:.2f}')
        chr.canvas.draw()

    def clear_data(self):
        for key in self.data.keys():
            self.data[key].clear()
        self.games.clear()
        
        self.update_chart(self.stat_cv1, self.games, self.data[self._chart1_var.get()])
        self.update_chart(self.stat_cv2, self.games, self.data[self._chart2_var.get()])
        self._last_games.config(state=tk.NORMAL)
        self._last_games.delete("1.0", tk.END)
        self._last_games.config(state=tk.DISABLED)
        self._averages.config(state=tk.NORMAL)
        self._averages.delete("1.0", tk.END)
        self._averages.config(state=tk.DISABLED)
        #self.stat_cv3.ax.clear()
        #self.stat_cv3.canvas.draw()

    def statistics(self, parameters):
        #print(parameters)

        self.data["points"].append(parameters[0])
        self.data["turns"].append(parameters[1])
        self.data["times"].append(parameters[2])

        if len(self.games) == 0:
            self.games.append(1)
        else:
            self.games.append(self.games[-1] + 1)

        self.update_consoles()
        self.update_chart(self.stat_cv1, self.games, self.data[self._chart1_var.get()])
        self.update_chart(self.stat_cv2, self.games, self.data[self._chart2_var.get()])
        #rat = [self.data[self._chart1_var.get()][i]/self.data[self._chart2_var.get()][i]
                #for i in range(len(self.data["points"]))]
        #self.update_chart(self.stat_cv3, self.games, rat)
    
    def save_data(self):
        df = pd.DataFrame(self.data)
        file = tk.filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Zapisz jako")

        if file:
            df.to_csv(file, index=False, sep=';')

    def update_consoles(self):
        max_lines = 10
        if not self.games:
            return
        
        new_line = f"game number {self.games[-1]}: points = {self.data['points'][-1]}, turns = {self.data['turns'][-1]}, total time = {self.data['times'][-1]}"
        current_text = self._last_games.get("1.0", tk.END).strip().split('\n')

        if current_text == ['']:
            current_text = []

        current_text.insert(0, new_line)
        current_text = current_text[:max_lines]

        self._last_games.config(state=tk.NORMAL)
        self._last_games.delete("1.0", tk.END)
        self._last_games.insert(tk.END, '\n'.join(current_text))
        self._last_games.config(state=tk.DISABLED)
        ####################################
        self._averages.config(state=tk.NORMAL)
        self._averages.delete("1.0", tk.END)
        for key in self.data.keys():
            if len(self.data[key]):
                self._averages.insert(tk.END, f"avg {key}: {np.mean(self.data[key])}\n")
        self._averages.config(state=tk.DISABLED)



def main():
    snake = game.Game()
    root = GUI(snake)

if __name__ == "__main__":
    main()