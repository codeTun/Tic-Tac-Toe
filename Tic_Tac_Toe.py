import tkinter as tk
from tkinter import Button, messagebox
from tkinter import ttk


class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.difficulty = tk.StringVar()
        self.difficulty.set("Easy")
        self.create_widgets()
        MenuFrame =  ttk.Frame(root)
        BuEasy   = Button(MenuFrame,text="Easy",width=50)
        BuMedium = Button(MenuFrame,text="Hard",width=50)
        BuUser   = Button(MenuFrame,text="User2",width=50)

        BuEasy.pack()
        BuMedium.pack()
        BuUser.pack()

    def create_widgets(self):
        self.info_label = tk.Label(self.master, text=f"Player {self.current_player}'s turn")
        self.info_label.grid(row=0, column=0, columnspan=3)

        self.difficulty_label = tk.Label(self.master, text="Difficulty")
        self.difficulty_label.grid(row=1, column=0)

        self.easy_difficulty_button = tk.Radiobutton(self.master, text="Easy", variable=self.difficulty, value="Easy")
        self.easy_difficulty_button.grid(row=1, column=1)

        self.medium_difficulty_button = tk.Radiobutton(self.master, text="Hard", variable=self.difficulty, value="Medium")
        self.medium_difficulty_button.grid(row=1, column=2)

        self.hard_difficulty_button = tk.Radiobutton(self.master, text="User2", variable=self.difficulty, value="Hard")
        self.hard_difficulty_button.grid(row=1, column=3)

        self.buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(self.master, text=' ', font=('Arial', 20), width=5, height=2,
                                   command=lambda row=row, col=col: self.handle_click(row, col))
                button.grid(row=row + 2, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def handle_click(self, row, col):
        if self.board[row * 3 + col] == ' ' and not self.check_win():
            self.board[row * 3 + col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_win():
                self.show_message(f"Player {self.current_player} wins!")
            elif self.check_tie():
                self.show_message("It's a tie!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.info_label.config(text=f"Player {self.current_player}'s turn")
                if self.current_player == 'O':
                    self.master.after(1000, self.computer_move)

    def computer_move(self):
        if self.difficulty.get() == "Easy":
            available_moves = [i for i in range(9) if self.board[i] == ' ']
            index = available_moves[0]
        elif self.difficulty.get() == "Medium":
            available_moves = [i for i in range(9) if self.board[i] == ' ']
            for player in ['O', 'X']:
                for move in available_moves:
                    board_copy = self.board[:]
                    board_copy[move] = player
                    if self.check_win(board_copy, player):
                        index = move
                        break
                else:
                    continue
                break
            else:
                index = available_moves[0]
        else:
            index = self.minimax(self.board, 'O')
        row, col = index // 3, index % 3
        self.board[index] = 'O'
        self.buttons[row][col].config(text='O')
        if self.check_win():
            self.show_message("Computer wins!")
        elif self.check_tie():
            self.show_message("It's a tie!")
        else:
            self.current_player = 'X'
            self.info_label.config(text=f"Player {self.current_player}'s turn")

    def check_win(self, board=None, player=None):
        if board is None:
            board = self.board
        if player is None:
            player = self.current_player
        for i in range(0, 9, 3):
            if board[i] == board[i + 1] == board[i + 2] == player:
                return True
        for i in range(3):
            if board[i] == board[i + 3] == board[i + 6] == player:
                return True
        if board[0] == board[4] == board[8] == player:
            return True
        if board[2] == board[4] == board[6] == player:
            return True
        return False

    def check_tie(self):
        return ' ' not in self.board and not self.check_win()

    def show_message(self, message):
        messagebox.showinfo("Tic Tac Toe", message)
        self.master.destroy()

    def minimax(self, board, player):
        if self.check_win(board, 'X'):
            return None, -10
        elif self.check_win(board, 'O'):
            return None, 10
        elif self.check_tie(board):
            return None, 0

        if player == 'O':
            best_move = None
            best_score = -100
        else:
            best_move = None
            best_score = 100

        for move in range(9):
            if board[move] == ' ':
                board[move] = player
                score = self.minimax(board, 'O' if player == 'X' else 'X')[1]
                board[move] = ' '
                if player == 'O' and score > best_score:
                    best_move = move
                    best_score = score
                elif player == 'X' and score < best_score:
                    best_move = move
                    best_score = score
        return best_move, best_score
root = tk.Tk()
app = TicTacToe(root)
root.mainloop()
