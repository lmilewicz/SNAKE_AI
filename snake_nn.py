# -*- coding: utf-8 -*-

from keras.models import Sequential
from keras.layers import Dense
import random

import numpy as np


class SnakeNetwork:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(5, activation='relu', input_shape=(5,)))
        self.model.add(Dense(15, activation='relu'))  # ,  input_shape=(5,)
        # self.model.add(Dense(10, activation='relu'))  # ,  input_shape=(15,)
        self.model.add(Dense(3, activation='softmax'))  # ,  input_shape=(1,)
        self.model.compile(optimizer='rmsprop', loss='mse', metrics=['accuracy'])

    def predict_action(self, x):
        output_prob = self.model.predict(x)
        # print(output_prob)
        return np.argmax(output_prob)


def model_mutate(weights):  # , generation
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if random.uniform(0, 1) > 0.85:
                change = random.uniform(-0.5, 0.5)
                weights[i][j] += change
    return weights


def calculate_fitness(score, steps):
    return steps+(2**score+(score**2.1)*500)-(((max(1, score))**1.2)*(0.25*steps)**1.5)


def model_crossover(parent1, parent2):
    weight1 = parent1.model.get_weights()
    weight2 = parent2.model.get_weights()

    new_weight1 = weight1
    new_weight2 = weight2

    gene = random.randint(0, len(weight1) - 1)

    new_weight1[gene] = weight2[gene]
    new_weight2[gene] = weight1[gene]

    return np.asarray([new_weight1, new_weight2])
