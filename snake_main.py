# -*- coding: utf-8 -*-

from random import randint
import numpy as np
import time

from snake_game import SnakeGame
from snake_nn import *
from utils import *


def generate_new_population(n):
    snakes_population = n*[None]
    start = time.time()
    for i in range(n):
        snakes_population[i] = SnakeNetwork()
        print_progress("generateNewPopulation", i, n, start)
    print("\n")
    return snakes_population


def play_game(z, n, snakes_population):
    fitness_array = np.zeros(n)
    start = time.time()
    best_score = 0
    for i, snake in enumerate(snakes_population):
        game = SnakeGame()
        x = game.start()
        prev_score = score = 0
        prev_j = 0
        for j in range(400):
            [x, score, end] = game.step(snake.predict_action(x))
            if score > prev_score:
                prev_score = score
                prev_j = j
            if end > 0 or j - 100 > prev_j:
                break
        if score > best_score:
            best_score = score
        fitness_array[i] = calculate_fitness(score, j)
        print_progress("Snake game", i, len(snakes_population), start)
    print("\nBest score for generation %d: %d. Fitness: %d. Median: %d. Time: %0.2f\n" %
          (z, best_score, np.max(fitness_array), np.median(fitness_array), time.time()-start))

    return fitness_array


def run_generations(n, generations, model_filename):
    parent1 = SnakeNetwork()
    snakes_population = generate_new_population(n)

    for z in range(generations):
        fitness_array = play_game(z, n, snakes_population)
        if np.max(fitness_array) <= 0:
            print("Snake population from scratch")
            snakes_population = generate_new_population(n)
        else:
            parent1 = snakes_population[np.argmax(fitness_array)]
            fitness_array[np.argmax(fitness_array)] = -1
            if np.max(fitness_array) > 0:
                parent2 = snakes_population[np.argmax(fitness_array)]
            else:
                parent2 = snakes_population[randint(0, len(snakes_population) - 1)]
            for x, child in enumerate(snakes_population):
                child.model.set_weights(model_crossover(parent1, parent2)[randint(0, 1)])
                child.model.set_weights(model_mutate(child.model.get_weights()))

    save_model(parent1.model, model_filename)


def main(n, generations, load_and_play, model_filename):
    if load_and_play == 0:
        run_generations(n, generations, model_filename)
    else:
        parent = SnakeNetwork()
        parent.model = load_saved_model(model_filename)
        # if z % 20 == 19:
        game = SnakeGame(gui=True)
        x = game.start()
        for j in range(100):
            [x, score, end] = game.step(parent.predict_action(x))
            if end > 0:
                break


if __name__ == "__main__":
    main(200, 50, 0, "model_2")
