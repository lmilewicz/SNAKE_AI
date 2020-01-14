# -*- coding: utf-8 -*-

from keras.models import Sequential
from keras.layers import Dense
import random

import numpy as np


class SnakeNetwork:
    def __init__(self):
        self.fitness = 0
        self.default_lifespan = 100
        self.mutation_rate = 0.05
        self.mutation_scale = 0.5
        self.SBX_eta = 10
        self.SBX_prob = 0.5
        self.lifespan = self.default_lifespan
        self.model = Sequential()
        self.model.add(Dense(8, activation='relu', input_shape=(8,)))
        self.model.add(Dense(14, activation='relu'))  # ,  input_shape=(8,)
        self.model.add(Dense(20, activation='relu'))  # ,  input_shape=(8,)
        self.model.add(Dense(9, activation='relu'))  # ,  input_shape=(14,)
        self.model.add(Dense(3, activation='softmax'))  # ,  input_shape=(8,)
        self.model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    def predict_action(self, x):
        output_prob = self.model.predict(x)
        # print(output_prob)
        return np.argmax(output_prob)

    def set_fitness(self, _fitness):
        self.fitness = _fitness


def calculate_fitness(score, steps):
    return steps + (2 ** score + (score ** 2.1) * 500) - (((max(1, score)) ** 1.2) * (0.25 * steps) ** 1.3)


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


def single_point_binary_crossover(parent1, parent2):
    weight1 = parent1.model.get_weights()
    weight2 = parent2.model.get_weights()

    chromosome1 = weight1
    chromosome2 = weight2

    gene = random.randint(0, len(weight1) - 1)

    chromosome1[gene] = weight2[gene]
    chromosome2[gene] = weight1[gene]

    return np.asarray([chromosome1, chromosome2])


def simulated_binary_crossover(parent1, parent2, SBX_eta):
    weight1 = np.asarray(parent1.model.get_weights())
    weight2 = np.asarray(parent2.model.get_weights())
    rand = np.random.random(weight1.shape)
    gamma = np.empty(weight1.shape)
    gamma[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1.0 / (SBX_eta + 1))
    gamma[rand > 0.5] = (1.0 / (2.0 * (1.0 - rand[rand > 0.5]))) ** (1.0 / (SBX_eta + 1))

    chromosome1 = 0.5 * ((1 + gamma) * weight1 + (1 - gamma) * weight2)
    chromosome2 = 0.5 * ((1 - gamma) * weight1 + (1 + gamma) * weight2)

    return np.asarray([chromosome1, chromosome2])


def model_mutate(chromosome, prob_mutation, scale):
    for i in range(len(chromosome)):
        for j in range(len(chromosome[i])):
            if random.uniform(0, 1) < prob_mutation:
                change = random.uniform(-scale, scale)
                chromosome[i][j] += change
    # mutation_array = np.random.random(chromosome.shape) < prob_mutation
    # mutation_factor = np.random.normal(size=chromosome.shape)
    # if scale > 0:
    #     mutation_factor[mutation_array] *= scale
    # chromosome[mutation_array] += mutation_factor[mutation_array]
    return chromosome


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
        if np.random.random() < snake.SBX_prob:
            [c1_w, c2_w] = simulated_binary_crossover(p1, p2, snake.SBX_eta)
        else:
            [c1_w, c2_w] = single_point_binary_crossover(p1, p2)
        # c1_w = model_mutate(c1_w)
        # c2_w = model_mutate(c2_w)
        c1_w = model_mutate(c1_w, snake.mutation_rate, snake.mutation_scale)
        c2_w = model_mutate(c2_w, snake.mutation_rate, snake.mutation_scale)

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
