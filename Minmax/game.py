import random
import copy
import math
from timeit import default_timer as timer

HOLES_AMOUNT = 14
PLAYER_ONE = -1
PLAYER_TWO = 0
COUNTER_FIRST, COUNTER_SECOND = 0, 0
MOVES_ONE, MOVES_TWO = 0, 0


class Hole:

    def __init__(self, number):
        self.stones = 4
        self.hole_number = number
        self.opposite_hole = None
        self.next_hole = None

    def move_stones(self, player_turn):
        moving_stones = self.stones
        self.stones = 0
        if moving_stones > 0:
            return Hole.take_stone_and_go_on(self.next_hole, moving_stones, player_turn)

    @staticmethod
    def take_stone_and_go_on(hole, remaining_stones, player_turn):
        if remaining_stones == 1:
            if (player_turn == PLAYER_ONE and hole.hole_number == -1) or (player_turn == PLAYER_TWO and hole.hole_number == 0):
                hole.next_hole.stones += 1
                return hole.next_hole.hole_number
            else:
                hole.stones += 1
                return hole.hole_number
        if (player_turn == PLAYER_ONE and hole.hole_number == -1) or (player_turn == PLAYER_TWO and hole.hole_number == 0):
            return Hole.take_stone_and_go_on(hole.next_hole, remaining_stones, player_turn)
        else:
            hole.stones += 1
            return Hole.take_stone_and_go_on(hole.next_hole, remaining_stones - 1, player_turn)


class Board:

    def __init__(self):
        self.player_turn = random.choice([PLAYER_ONE, PLAYER_TWO])
        self.holes = [Hole(-1), Hole(1), Hole(2), Hole(3), Hole(4), Hole(5),
                      Hole(6), Hole(0), Hole(7), Hole(8), Hole(9), Hole(10),
                      Hole(11), Hole(12)]
        self.holes[7].stones = 0
        self.holes[0].stones = 0
        self.set_next_holes()
        self.set_opposite_holes()

    def set_next_holes(self):
        for i in range(HOLES_AMOUNT - 1):
            self.holes[i].next_hole = self.holes[i+1]
        self.holes[HOLES_AMOUNT - 1].next_hole = self.holes[0]

    def set_opposite_holes(self):
        for i in range(1, int(HOLES_AMOUNT / 2)):
            self.holes[i].opposite_hole = self.holes[HOLES_AMOUNT - i]
            self.holes[HOLES_AMOUNT - i].opposite_hole = self.holes[i]

    def decide_turn(self, current_hole_number):
        if self.player_turn == PLAYER_ONE:
            if current_hole_number != 0:
                self.player_turn = PLAYER_TWO
        else:
            if current_hole_number != -1:
                self.player_turn = PLAYER_ONE

    def check_if_the_game_is_finished(self):
        # start_hole = 1
        # end_hole = 7
        # if self.player_turn == PLAYER_TWO:
        #     start_hole = 8
        #     end_hole = 14
        # for i in range(start_hole, end_hole):
        #     if self.holes[i].stones != 0:
        #         return False
        # self.add_remaining_stones_to_winners_well()
        # return True
        if all(hole.stones == 0 for hole in self.holes[1:7]):
            added_stones = 0
            for hole in self.holes[8:14]:
                added_stones += hole.stones
                hole.stones = 0
            self.holes[0].stones += added_stones
            return True
        elif all(hole.stones == 0 for hole in self.holes[8:14]):
            added_stones = 0
            for hole in self.holes[1:7]:
                added_stones += hole.stones
                hole.stones = 0
            self.holes[7].stones += added_stones
            return True
        return False

    @staticmethod
    def h1_heuristic(board, starting_player):
        if starting_player == PLAYER_ONE:
            return board.holes[6].stones
        else:
            return board.holes[13].stones

    @staticmethod
    def heuristic_evaluate(board, number_of_moves, starting_player):
        sign = 1
        if starting_player == PLAYER_TWO:
            sign = -1
        right_hole = Board.h1_heuristic(board, starting_player)
        # right_hole = 0
        return 3 * (board.holes[7].stones - board.holes[0].stones) + (0.161 * right_hole * sign) + (0.29 * number_of_moves * sign)

    def add_remaining_stones_to_winners_well(self):
        start_hole = 1
        end_hole = 7
        winners_well_index = 7
        if self.player_turn == PLAYER_ONE:
            start_hole = 8
            end_hole = 14
            winners_well_index = 0
        for i in range(start_hole, end_hole):
            self.holes[winners_well_index].stones += self.holes[i].stones
            self.holes[i].stones = 0

    def check_if_stone_takes_opposite_hole(self, hole_number):
        if (self.player_turn == PLAYER_ONE and 1 <= hole_number < 7) or (self.player_turn == PLAYER_TWO and 7 <= hole_number <= 12):
            if hole_number > 6:
                hole_number += 1
            if self.holes[hole_number].opposite_hole is not None and self.holes[hole_number].stones == 1:
                stones_in_opposite = self.holes[hole_number].opposite_hole.stones
                if stones_in_opposite > 1:
                    self.holes[hole_number].opposite_hole.stones = 0
                    self.holes[hole_number].stones = 0
                    if self.player_turn == PLAYER_ONE:
                        self.holes[7].stones += stones_in_opposite + 1
                    else:
                        self.holes[0].stones += stones_in_opposite + 1

    def get_available_moves(self):
        available_moves = self.get_potential_moves()
        updated_moves = []
        Board.include_additional_move(self, available_moves, updated_moves)
        return updated_moves

    def get_potential_moves(self):
        start_hole = 1
        end_hole = 7
        if self.player_turn == PLAYER_TWO:
            start_hole = 8
            end_hole = 14
        potential_moves = []
        for i in range(start_hole, end_hole):
            if self.holes[i].stones > 0:
                potential_moves.append([i])
        return potential_moves

    @staticmethod
    def include_additional_move(board, available_moves, updated_moves):
        for move in available_moves:
            last_element = move[-1]
            temp_board = copy.deepcopy(board)
            last_hole_number, is_game_finished = temp_board.move_stones_from_hole(last_element)
            if not is_game_finished and temp_board.does_move_reach_players_well(last_hole_number):
                potential_moves = temp_board.get_potential_moves()
                next_choices = []
                for potential in potential_moves:
                    next_choices.append(move + potential)
                Board.include_additional_move(temp_board, next_choices, updated_moves)
                del temp_board
            else:
                del temp_board
                updated_moves.append(move)

    def does_move_reach_players_well(self, last_hole_number):
        if self.player_turn == PLAYER_ONE:
            if last_hole_number == 0:
                return True
        elif self.player_turn == PLAYER_TWO:
            if last_hole_number == -1:
                return True
        return False

    def move_stones_from_hole(self, hole_index):
        last_hole_number = self.holes[hole_index].move_stones(self.player_turn)
        self.check_if_stone_takes_opposite_hole(last_hole_number)
        is_game_finished = self.check_if_the_game_is_finished()
        return last_hole_number, is_game_finished

    def ai_random_move(self):
        start_hole = 1
        end_hole = 6
        if not self.player_turn:
            start_hole = 8
            end_hole = 13
        r = random.randint(start_hole, end_hole)
        while self.holes[r].stones == 0:
            r = random.randint(start_hole, end_hole)
        return self.holes[r].move_stones(self.player_turn)

    def ai_minimax_move(self, depth):
        global MOVES_ONE, MOVES_TWO
        maximizing = True
        turn = 'Player\'s one choice: '
        if self.player_turn == PLAYER_TWO:
            maximizing = False
            turn = 'Player\'s two choice: '
        best_val, chosen_moves = Board.minimax(self, depth, maximizing)
        self.make_moves_from_list(chosen_moves)
        print(turn, best_val, chosen_moves)
        if self.player_turn == PLAYER_ONE:
            MOVES_ONE += len(chosen_moves)
            self.player_turn = PLAYER_TWO
        else:
            MOVES_TWO += len(chosen_moves)
            self.player_turn = PLAYER_ONE

    def ai_alpha_beta_move(self, depth):
        global MOVES_ONE, MOVES_TWO
        maximizing = True
        turn = 'Player\'s one choice: '
        if self.player_turn == PLAYER_TWO:
            maximizing = False
            turn = 'Player\'s two choice: '
        best_val, chosen_moves = Board.minimax_with_alpha_beta(self, depth, -math.inf, math.inf, maximizing)
        self.make_moves_from_list(chosen_moves)
        print(turn, best_val, chosen_moves)
        if self.player_turn == PLAYER_ONE:
            MOVES_ONE += len(chosen_moves)
            self.player_turn = PLAYER_TWO
        else:
            MOVES_TWO += len(chosen_moves)
            self.player_turn = PLAYER_ONE

    def ai_heuristics_move(self, depth):
        global MOVES_ONE, MOVES_TWO
        maximizing = True
        turn = 'Player\'s one choice: '
        if self.player_turn == PLAYER_TWO:
            maximizing = False
            turn = 'Player\'s two choice: '
        best_val, chosen_moves = Board.minimax_with_alpha_beta_heuristics(self, depth, -math.inf, math.inf, maximizing, self.player_turn, 0)
        self.make_moves_from_list(chosen_moves)
        print(turn, best_val, chosen_moves)
        if self.player_turn == PLAYER_ONE:
            MOVES_ONE += len(chosen_moves)
            self.player_turn = PLAYER_TWO
        else:
            MOVES_TWO += len(chosen_moves)
            self.player_turn = PLAYER_ONE

    def make_moves_from_list(self, moves):
        for move in moves:
            self.move_stones_from_hole(move)

    @staticmethod
    def minimax(game, depth, is_maximizing):
        global COUNTER_FIRST, COUNTER_SECOND
        chosen_moves = []
        if depth == 0 or game.check_if_the_game_is_finished():
            return game.holes[7].stones - game.holes[0].stones, chosen_moves
        if is_maximizing:
            best_val = -math.inf
            for available_moves in game.get_available_moves():
                COUNTER_FIRST += 1
                game_copy = copy.deepcopy(game)
                game_copy.make_moves_from_list(available_moves)
                result = Board.minimax(game_copy, depth - 1, False)[0]
                del game_copy
                if result > best_val:
                    best_val = result
                    chosen_moves = available_moves
            return best_val, chosen_moves
        else:
            best_val = math.inf
            for available_moves in game.get_available_moves():
                COUNTER_SECOND += 1
                game_copy = copy.deepcopy(game)
                game_copy.make_moves_from_list(available_moves)
                result = Board.minimax(game_copy, depth - 1, True)[0]
                del game_copy
                if result < best_val:
                    best_val = result
                    chosen_moves = available_moves
            return best_val, chosen_moves

    @staticmethod
    def minimax_with_alpha_beta(game, depth, alpha, beta, is_maximizing):
        global COUNTER_FIRST, COUNTER_SECOND
        chosen_moves = []
        if depth == 0 or game.check_if_the_game_is_finished():
            return game.holes[7].stones - game.holes[0].stones, chosen_moves
        if is_maximizing:
            best_val = -math.inf
            for available_moves in game.get_available_moves():
                COUNTER_FIRST += 1
                game_copy = copy.deepcopy(game)
                game_copy.make_moves_from_list(available_moves)
                result = Board.minimax_with_alpha_beta(game_copy, depth - 1, alpha, beta, False)[0]
                del game_copy
                if result > best_val:
                    best_val = result
                    chosen_moves = available_moves

                alpha = max(alpha, result)
                if beta <= alpha:
                    break
            return best_val, chosen_moves
        else:
            best_val = math.inf
            for available_moves in game.get_available_moves():
                COUNTER_SECOND += 1
                game_copy = copy.deepcopy(game)
                game_copy.make_moves_from_list(available_moves)
                result = Board.minimax_with_alpha_beta(game_copy, depth - 1, alpha, beta, True)[0]
                del game_copy
                if result < best_val:
                    best_val = result
                    chosen_moves = available_moves

                beta = min(beta, result)
                if beta <= alpha:
                    break

            return best_val, chosen_moves

    @staticmethod
    def minimax_with_alpha_beta_heuristics(game, depth, alpha, beta, is_maximizing, starting_player, number_of_moves):
        global COUNTER_FIRST, COUNTER_SECOND
        chosen_moves = []
        if depth == 0 or game.check_if_the_game_is_finished():
            return Board.heuristic_evaluate(game, number_of_moves, starting_player), chosen_moves
        if is_maximizing:
            best_val = -math.inf
            for available_moves in game.get_available_moves():
                COUNTER_FIRST += 1
                game_copy = copy.deepcopy(game)
                game_copy.make_moves_from_list(available_moves)
                starts = True
                if starting_player == PLAYER_TWO:
                    starts = False
                if starts == is_maximizing:
                    number_of_moves += len(available_moves)
                result = Board.minimax_with_alpha_beta_heuristics(game_copy, depth - 1, alpha, beta, False, starting_player, number_of_moves)[0]
                del game_copy
                if result > best_val:
                    best_val = result
                    chosen_moves = available_moves

                alpha = max(alpha, result)
                if beta <= alpha:
                    break
            return best_val, chosen_moves
        else:
            best_val = math.inf
            for available_moves in game.get_available_moves():
                COUNTER_SECOND += 1
                game_copy = copy.deepcopy(game)
                game_copy.make_moves_from_list(available_moves)
                starts = True
                if starting_player == PLAYER_TWO:
                    starts = False
                if starts == is_maximizing:
                    number_of_moves += len(available_moves)
                result = Board.minimax_with_alpha_beta_heuristics(game_copy, depth - 1, alpha, beta, True, starting_player, number_of_moves)[0]
                del game_copy
                if result < best_val:
                    best_val = result
                    chosen_moves = available_moves

                beta = min(beta, result)
                if beta <= alpha:
                    break

            return best_val, chosen_moves

    def visualize_board(self):
        for hole in self.holes[1:7]:
            print(' ' + str(hole.stones) + ' ', end='')
        print('\n' + str(self.holes[0].stones) + 15 * ' ' + str(self.holes[7].stones))
        for hole in self.holes[13:7:-1]:
            print(' ' + str(hole.stones) + ' ', end='')
        print('\n')

    def ai_simulation(self):
        end = False
        while not end:
            print(self.get_available_moves())
            print(Board.minimax(self, 5, self.player_turn))
            last = self.ai_random_move()
            self.check_if_stone_takes_opposite_hole(last)
            self.decide_turn(last)
            end = self.check_if_the_game_is_finished()
        print("The game has ended!")
        print("AI 1 score: ", self.holes[7].stones)
        print("AI 2 score: ", self.holes[0].stones)

    def ai_simulation_minimax(self, depth):
        last = self.ai_random_move()
        self.check_if_stone_takes_opposite_hole(last)
        self.decide_turn(last)
        end = self.check_if_the_game_is_finished()
        while not end:
            Board.ai_minimax_move(self, depth)
            self.visualize_board()
            end = self.check_if_the_game_is_finished()
        print("The game has ended!")
        print("AI 1 score: ", self.holes[7].stones)
        print("AI 2 score: ", self.holes[0].stones)

    def ai_simulation_alpha_beta(self, depth):
        last = self.ai_random_move()
        self.check_if_stone_takes_opposite_hole(last)
        self.decide_turn(last)
        end = self.check_if_the_game_is_finished()
        while not end:
            Board.ai_alpha_beta_move(self, depth)
            self.visualize_board()
            end = self.check_if_the_game_is_finished()
        print("The game has ended!")
        print("AI 1 score: ", self.holes[7].stones)
        print("AI 2 score: ", self.holes[0].stones)

    def ai_simulation_heuristics(self, depth):
        last = self.ai_random_move()
        self.check_if_stone_takes_opposite_hole(last)
        self.decide_turn(last)
        end = self.check_if_the_game_is_finished()
        while not end:
            Board.ai_heuristics_move(self, depth)
            self.visualize_board()
            end = self.check_if_the_game_is_finished()
        print("The game has ended!")
        print("AI 1 score: ", self.holes[7].stones)
        print("AI 2 score: ", self.holes[0].stones)


if __name__ == '__main__':
    avg_time = 0
    avg_moves = 0
    iters = 5
    for i in range(iters):
        b = Board()
        start = timer()
        b.ai_simulation_minimax(3)
        # b.ai_simulation_alpha_beta(3)
        # b.ai_simulation_heuristics(4)
        end = timer()
        avg_time += (end - start)
        print(end - start)
        print(COUNTER_FIRST, COUNTER_SECOND)
        if b.holes[0].stones > b.holes[7].stones:
            avg_moves += COUNTER_SECOND
        else:
            avg_moves += COUNTER_FIRST
        COUNTER_SECOND, COUNTER_FIRST = 0, 0
        print('-----------------------------------')
    print(avg_time / iters)
    print(avg_moves / iters)
    # b = Board()
    # b1 = Board()
    # b.ai_simulation_minimax(3)
    print('-------------------------')
    print(MOVES_ONE / iters, MOVES_TWO / iters)
    # b1.ai_simulation_heuristics(4)
