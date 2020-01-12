# -*- coding: utf-8 -*-

from keras.models import Sequential
from keras.layers import Dense
import random

import numpy as np


class SnakeNetwork:
    def __init__(self):
        self.fitness = 0
        self.default_lifespan = 20
        self.lifespan = self.default_lifespan
        self.model = Sequential()
        self.model.add(Dense(8, activation='relu', input_shape=(8,)))
        self.model.add(Dense(20, activation='relu'))  # ,  input_shape=(5,)
        self.model.add(Dense(10, activation='relu'))  # ,  input_shape=(15,)
        self.model.add(Dense(3, activation='softmax'))  # ,  input_shape=(1,)
        self.model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    def predict_action(self, x):
        output_prob = self.model.predict(x)
        # print(output_prob)
        return np.argmax(output_prob)

    def set_fitness(self, _fitness):
        self.fitness = _fitness


def calculate_fitness(score, steps):
    return steps + (2 ** score + (score ** 2.1) * 500) - (((max(1, score)) ** 1.2) * (0.25 * steps) ** 1.5)


def elitism_selection(snake_population, snakes_num):
    snake_population.sort(key=lambda snake: snake.fitness, reverse=True)
    return snake_population[:snakes_num]


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


def model_crossover(parent1, parent2):
    weight1 = parent1.model.get_weights()
    weight2 = parent2.model.get_weights()

    new_weight1 = weight1
    new_weight2 = weight2

    gene = random.randint(0, len(weight1) - 1)

    new_weight1[gene] = weight2[gene]
    new_weight2[gene] = weight1[gene]

    return np.asarray([new_weight1, new_weight2])


def model_mutate(weights):  # , generation
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if random.uniform(0, 1) > 0.85:
                change = random.uniform(-0.5, 0.5)  # *np.max(weights[i])
                weights[i][j] += change
    return weights


def next_generation(snakes_population, elite_size):
    new_population = snakes_population
    snakes_elite = elitism_selection(snakes_population, max(2, elite_size))

    snakes_added = 0
    for snake in snakes_elite:
        snake.lifespan -= 1
        if snake.lifespan > 0:
            new_population[snakes_added].model.set_weights(snake.model.get_weights())
            snakes_added += 1

    while snakes_added < len(snakes_population):
        p1, p2 = roulette_wheel_selection(snakes_elite, 2)
        [c1_w, c2_w] = model_crossover(p1, p2)
        c1_w = model_mutate(c1_w)
        c2_w = model_mutate(c2_w)

        new_population[snakes_added].model.set_weights(c1_w)
        new_population[snakes_added].lifespan = new_population[snakes_added].default_lifespan
        new_population[snakes_added + 1].model.set_weights(c2_w)
        new_population[snakes_added + 1].lifespan = new_population[snakes_added].default_lifespan
        snakes_added += 2

        if snakes_added + 1 == len(snakes_population):
            random_snake = snakes_elite[random.randint(0, len(snakes_elite) - 1)]
            new_population[snakes_added].model.set_weights(random_snake.model.get_weights())
            snakes_added += 1

    random.shuffle(new_population)
    return new_population
