# This is game Tic-Tac-Toe with Minimax algorithm as a hard levle
# Author : Mateusz Gąsior


import numpy as np
import random as rd


class TicTacToe:
    def __init__(self):
        self.layout = np.zeros((3, 3))
        self.num_o = 0
        self.num_x = 0
        self.display = []
        self.player1 = ''
        self.player2 = ''
        self.active_player = ''
        self.levels = ['user', 'easy', 'medium', 'hard']
        print('''To activate game choose insert start and what users will play.
                         E.g. 'start user easy' - means player 1 will be human and player 2 will be easy computer.
                        You can simulate game of two computers or you can play multiplayer
                        Coordinates looks like below:
                        (0,0) (0,1) (0,2)
                        (1,0) (1,1) (1,2)
                        (2,0) (2,1) (2,2)
        ''')

    def choose_game_mode(self):
        while True:
            mode = input('Input command: ').split()
            if mode[0] == 'exit':
                exit()
            else:
                if mode[0] == 'start':
                    if len(mode) == 3:
                        if (mode[1] in self.levels) and (mode[2] in self.levels):
                            self.display_field()
                            self.player1 = mode[1]
                            self.player2 = mode[2]
                            self.active_player = self.player1
                            self.game_navigation()
                        else:
                            print('Bad parameters!')
                            continue
                    else:
                        print('Bad parameters!')
                        continue
                else:
                    print('Bad parameters!')

    def game_navigation(self):
        if self.active_player == 'user':
            move = self.next_move()
            self.making_move(move[0], move[1])
        elif self.active_player == 'easy':
            self.easy_ai_move()
        elif self.active_player == 'medium':
            self.medium_ai_move()
        elif self.active_player == 'hard':
            self.hard_ai_move()

    def display_field(self) -> None:
        boarder = ['-' * 9]
        for row in self.layout:
            d_row = []
            for a in row:
                if a == 0:
                    d_row.append(' ')
                elif a == 1:
                    d_row.append('O')
                elif a == 2:
                    d_row.append('X')
            self.display.append(d_row)
        out_str = boarder + [" ".join(['|'] + row + ['|']) for row in self.display] + boarder
        print("\n".join(out_str))
        self.display = []

    def next_move(self) -> tuple:
        global index_a, index_b
        try:
            move = input("Enter the coordinates: >").replace(" ", "")
            if len(move) != 2:
                raise ValueError
            else:
                index_a = int(move[1])
                index_b = int(move[0])
                if not (0 <= index_a < 3 and 0 <= index_b < 3):
                    raise BufferError
                elif self.layout[index_a][index_b] != 0:
                    raise TypeError
        except ValueError:
            print("You should enter two numbers!")
            self.next_move()
        except BufferError:
            print("Coordinates should be from 1 to 3!")
            self.next_move()
        except TypeError:
            print("This cell is occupied! Choose another one!")
            self.next_move()
        finally:
            return index_a, index_b

    def making_move(self, pos_a, pos_b):
        if self.num_x <= self.num_o:
            self.layout[pos_a][pos_b] = 2
            self.num_x += 1
            self.active_player = self.player2
        else:
            self.layout[pos_a][pos_b] = 1
            self.num_o += 1
            self.active_player = self.player1
        self.display_field()
        self.check_result(self.layout)
        self.game_navigation()

    @staticmethod
    def check_result(layout, last_check=True):
        for i in range(3):
            if all(layout[i] == 2) or all(np.rot90(layout)[i] == 2):
                if last_check:
                    print("X wins")
                    exit()
                else:
                    return 10
            elif all(layout[i] == 1) or all(np.rot90(layout)[i] == 1):
                if last_check:
                    print("O wins")
                    exit()
                else:
                    return -10
        if all(layout.diagonal() == 2) or all(np.fliplr(layout).diagonal() == 2):
            if last_check:
                print("X wins")
                exit()
            else:
                return 10
        elif all(layout.diagonal() == 1) or all(np.fliplr(layout).diagonal() == 1):
            if last_check:
                print("O wins")
                exit()
            else:
                return -10
        elif not 0 in layout:
            if last_check:
                print("Draw")
                exit()
            else:
                return 0

    def medium_strategy_player(self, num) -> tuple:
        for i in range(3):
            if np.count_nonzero(self.layout[i] == num) == 2 and 0 in self.layout[i]:
                b = np.where(self.layout[i] == 0)[0][0]
                return i, b
            elif np.count_nonzero(np.rot90(self.layout)[i] == num) == 2 and 0 in np.rot90(self.layout)[i]:
                a = np.where(np.rot90(self.layout)[i] == 0)[0][0]
                return a, (2 - i)
        if np.count_nonzero(self.layout.diagonal() == num) == 2 and 0 in self.layout.diagonal():
            a = np.where(self.layout.diagonal() == 0)[0][0]
            return a, a
        elif np.count_nonzero(np.fliplr(self.layout).diagonal() == num) == 2 and 0 in np.fliplr(self.layout).diagonal():
            a = np.where(np.fliplr(self.layout).diagonal() == 0)[0][0]
            return a, (2 - a)
        else:
            return None

    def easy_ai_move(self):
        print('Making move level "easy"')
        move = rd.choice(self.get_possible_moves(self.layout))
        self.making_move(move[0], move[1])

    def medium_ai_move(self):
        print('Making move level "medium"')
        move_1, move_2 = self.medium_strategy_player(2), self.medium_strategy_player(1)
        if (self.player1 == 'medium' and move_1 is not None) or \
                (self.player2 == 'medium' and move_2 is None and move_1 is not None):
            move = move_1
        elif (self.player1 == 'medium' and move_1 is None and move_2 is not None) or \
                (self.player2 == 'medium' and move_2 is not None):
            move = move_2
        else:
            move = rd.choice(self.get_possible_moves(self.layout))
        self.making_move(move[0], move[1])

    @staticmethod
    def get_possible_moves(temp_layout):
        possible_moves = []
        for x in range(0, 3):
            for y in range(0, 3):
                if temp_layout[x][y] == 0:
                    possible_moves.append((x, y))
        return possible_moves

    def hard_ai_move(self):
        temp_layout = self.layout
        print("In progrss")
        exit()
        move = self.minimax_algorithm(temp_layout)

    def minimax_algorithm(self, temp_layout):
        print("In progrss")
        possible_moves = self.get_possible_moves(temp_layout)
        value = self.check_result(temp_layout, False)
        return a, b
        exit()


if __name__ == "__main__":
    TicTacToe().choose_game_mode()
