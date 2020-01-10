# -*- coding: utf-8 -*-

from random import randint
import numpy as np
import time
import sys

from snake_game import SnakeGame
from snake_nn import *


def print_progress(name, i, n, start):
    sys.stdout.write(
        "\r%s progress: %0.2f percent. Execution time: %0.2f" % (name, 100 * (i + 1) / n, time.time() - start))
    sys.stdout.flush()


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


if __name__ == "__main__":
    n = 500
    parent1 = SnakeNetwork()
    score = 0

    snakes_population = generate_new_population(n)
    # while score < 2:
    #    snakes_population = generate_new_population(n)
    #    score_array = play_game(-1, n, snakes_population)
    #    score = np.max(score_array)

    for z in range(1000):
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

        # if z % 20 == 19:
        #     game = SnakeGame(gui=True)
        #     x = game.start()
        #     for j in range(100):
        #         [x, score, end] = game.step(parent1.predict_action(x))
        #         if end > 0:
        #             break

    # serialize model to JSON
    model_json = parent1.model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    parent1.model.save_weights("model.h5")
    print("Saved model to disk")
