# -*- coding: utf-8 -*-

import curses
from random import randint
import numpy as np


class SnakeGame:
    def __init__(self, board_width=20, board_height=20, gui=False):
        self.snake = []
        self.food = []
        self.score = 0
        self.win = None
        self.done = False
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui

    def start(self):
        self.snake_init()
        self.generate_food()
        if self.gui: self.render_init()
        # return self.generate_observations()
        return self.input_coordinates()

    def snake_init(self):
        # x = randint(5, self.board["width"] - 5)
        # y = randint(5, self.board["height"] - 5)
        x = 10
        y = 10
        vertical = 0 == 0  # randint(0,1) == 0
        point = [x, y] if vertical else [x, y]
        for i in range(3):
            point = [x + i, y] if vertical else [x, y + i]
            self.snake.insert(0, point)

    def generate_food(self):
        food = []
        while not food:
            food = [randint(1, self.board["width"]), randint(1, self.board["height"])]
            if food in self.snake: food = []
        self.food = food

    def render_init(self):
        curses.initscr()
        win = curses.newwin(self.board["width"] + 2, self.board["height"] + 2, 0, 0)
        curses.curs_set(0)
        win.nodelay(1)
        win.timeout(200)
        self.win = win
        self.render()

    def render(self):
        self.win.clear()
        self.win.border(0)
        self.win.addstr(0, 2, 'Score : ' + str(self.score) + ' ')
        self.win.addch(self.food[0], self.food[1], '8')
        for i, point in enumerate(self.snake):
            if i == 0:
                self.win.addch(point[0], point[1], 'O')
            else:
                self.win.addch(point[0], point[1], 'x')
        self.win.getch()

    # def step(self, key):
    #     # 0 - UP
    #     # 1 - RIGHT
    #     # 2 - DOWN
    #     # 3 - LEFT
    #     if self.done: return self.end_game()
    #     self.create_new_point(key)
    #     if self.food_eaten():
    #         self.score += 1
    #         self.generate_food()
    #     else:
    #         self.remove_last_point()
    #         self.check_collisions()
    #     if self.gui: self.render()
    #     # return self.generate_observations()
    #     return [self.input_coordinates(), -1]
    #
    # def create_new_point(self, key):
    #     new_point = [self.snake[0][0], self.snake[0][1]]
    #     if key == 0:
    #         new_point[0] -= 1
    #     elif key == 1:
    #         new_point[1] += 1
    #     elif key == 2:
    #         new_point[0] += 1
    #     elif key == 3:
    #         new_point[1] -= 1
    #     self.snake.insert(0, new_point)

    def step(self, key):
        # 0 - LEFT
        # 1 - CONTINUE
        # 2 - RIGHT
        if self.done: return self.end_game()
        self.create_new_point(key)
        if self.food_eaten():
            self.score += 1
            self.generate_food()
        else:
            self.remove_last_point()
            self.check_collisions()
        if self.gui: self.render()
        # return self.generate_observations()
        return [self.input_coordinates(), self.score, 0]

    def create_new_point(self, key):
        new_point = [self.snake[0][0], self.snake[0][1]]
        prev_point = [self.snake[1][0], self.snake[1][1]]

        # direction:
        # 0 - UP
        # 1 - RIGHT
        # 2 - DOWN
        # 3 - LEFT
        if new_point[0]-prev_point[0] < 0:
            prev_direction = 0
        elif new_point[1]-prev_point[1] > 0:
            prev_direction = 1
        elif new_point[0]-prev_point[0] > 0:
            prev_direction = 2
        elif new_point[1]-prev_point[1] < 0:
            prev_direction = 3
        if key == 0:
            new_direction = prev_direction-1
            if new_direction == -1:
                new_direction = 3
        elif key == 1:
            new_direction = prev_direction
        elif key == 2:
            new_direction = prev_direction+1
            if new_direction == 4:
                new_direction = 0
        if new_direction == 0:
            new_point[0] -= 1
        elif new_direction == 1:
            new_point[1] += 1
        elif new_direction == 2:
            new_point[0] += 1
        elif new_direction == 3:
            new_point[1] -= 1
        self.snake.insert(0, new_point)

    def remove_last_point(self):
        self.snake.pop()

    def food_eaten(self):
        return self.snake[0] == self.food

    def check_collisions(self):
        if (self.snake[0][0] == 0 or
                self.snake[0][0] == self.board["width"] + 1 or
                self.snake[0][1] == 0 or
                self.snake[0][1] == self.board["height"] + 1 or
                # self.snake[0] in self.snake[1:-1] or
                self.snake[0] == self.snake[2][:]
                ):
            self.done = True

    # def input_coordinates(self):
    #     x = [self.snake[0][0] / self.board["height"], self.snake[0][1] / self.board["width"],
    #          (self.board["height"] - self.snake[0][0]) / self.board["height"],
    #          (self.board["width"] - self.snake[0][1]) / self.board["width"],
    #          (self.food[0] - self.snake[0][0]) / self.board["height"],
    #          (self.food[1] - self.snake[0][1]) / self.board["width"],
    #          (self.snake[len(self.snake) - 1][0] - self.snake[0][0]) / self.board["height"],
    #          (self.snake[len(self.snake) - 1][1] - self.snake[0][1]) / self.board["width"],
    #          (self.snake[int(len(self.snake) / 2)][0] - self.snake[0][0]) / self.board["height"],
    #          (self.snake[int(len(self.snake) / 2)][1] - self.snake[0][1]) / self.board["width"]]
    #     x = np.array(x)
    #     return x.reshape(1, 10)
    def input_coordinates(self):
        # 0 - distance from wall over left
        # 1 - distance from wall ahead
        # 2 - distance from wall over right
        # 3, 4 - distance from apple: x/y
        # 5 - distance from tail over left
        # 6 - distance from tail ahead
        # 7 - distance from tail over right
        if self.snake[0][0] - self.snake[1][0] < 0:
            # direction:
            # 0 - UP
            # 1 - RIGHT
            # 2 - DOWN
            # 3 - LEFT

            # direction = 0
            x = [self.snake[0][1] / self.board["width"],
                 self.snake[0][0] / self.board["height"],
                 (self.board["width"] - self.snake[0][1]) / self.board["width"],
                 (self.snake[0][0] - self.food[0]) / self.board["height"],
                 (self.food[1] - self.snake[0][1]) / self.board["width"]]
                 # (self.snake[len(self.snake) - 1][0] - self.snake[0][0]) / self.board["height"],
                 # (self.snake[len(self.snake) - 1][1] - self.snake[0][1]) / self.board["width"],
                 # (self.snake[int(len(self.snake) / 2)][0] - self.snake[0][0]) / self.board["height"],
                 # (self.snake[int(len(self.snake) / 2)][1] - self.snake[0][1]) / self.board["width"]]
        elif self.snake[0][1] - self.snake[1][1] > 0:
            # direction = 1
            x = [self.snake[0][0] / self.board["height"],
                 (self.board["width"] - self.snake[0][1]) / self.board["width"],
                 (self.board["height"] - self.snake[0][0]) / self.board["height"],
                 (self.food[1] - self.snake[0][1]) / self.board["width"],
                 (self.food[0] - self.snake[0][0]) / self.board["height"]]
        elif self.snake[0][0] - self.snake[1][0] > 0:
            # direction = 2
            x = [(self.board["width"] - self.snake[0][1]) / self.board["width"],
                 (self.board["height"] - self.snake[0][0]) / self.board["height"],
                 self.snake[0][1] / self.board["width"],
                 (self.food[0] - self.snake[0][0]) / self.board["height"],
                 (self.snake[0][1] - self.food[1]) / self.board["width"]]
        elif self.snake[0][1] - self.snake[1][1] < 0:
            # direction = 3
            x = [(self.board["height"] - self.snake[0][0]) / self.board["height"],
                 self.snake[0][1] / self.board["width"],
                 self.snake[0][0] / self.board["height"],
                 (self.snake[0][1] - self.food[1]) / self.board["width"],
                 (self.snake[0][0] - self.food[0]) / self.board["height"]]
        x = np.array(x)
        return x.reshape(1, 5)

    # def generate_observations(self):
    #    return self.done, self.score, self.snake, self.food

    def end_game(self):
        if self.gui:
            curses.endwin()
        # raise Exception("Game over")
        return [0, self.score, 1]
