# -*- coding: utf-8 -*-

import numpy as np
import random


def elitism_selection(snake_population, snakes_num):
    snakes_elite = snake_population.sort(key=lambda snake: snake.fitness, reverse=True)
    return snakes_elite[:snakes_num]


def roulette_wheel_selection(snake_population, snakes_num):
    selection = []
    wheel = sum(snake.fitness for snake in snake_population)
    for _ in range(snakes_num):
        pick = random.uniform(0, wheel)
        current = 0
        for snake in snake_population:
            current += snake.fitness
            if current > pick:
                selection.append(snake)
                break

    return selection


def tournament_selection(snake_population, snakes_num, tournament_size):
    selection = []
    for _ in range(snakes_num):
        tournament = np.random.choice(snake_population, tournament_size)
        best_from_tournament = max(tournament, key=lambda snake: snake.fitness)
        selection.append(best_from_tournament)

    return selection
