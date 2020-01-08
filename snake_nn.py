# -*- coding: utf-8 -*-

from keras.models import Sequential
from keras.layers import Dense
import random

import numpy as np

class SnakeNetwork:
    def __init__(self):
        self.create_model()
        
    def create_model(self):
        self.model = Sequential()
        self.model.add(Dense(10, activation='relu', input_shape=(10,)))
        self.model.add(Dense(20, activation='relu'))#,  input_shape=(10,)
        self.model.add(Dense(4, activation='softmax'))#,  input_shape=(20,)
        self.model.compile(optimizer='rmsprop', loss='mse', metrics=['accuracy'])

    def predict_action(self, x):
        output_prob = self.model.predict(x)
        #print(output_prob)
        return np.argmax(output_prob)

    def model_mutate(self, weights): #, generation    
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                if random.uniform(0,1) > 0.85:
                    change = random.uniform(-0.5, 0.5)
                    weights[i][j] += change
        return weights
    
def model_crossover(parent1, parent2):
    weight1 = parent1.model.get_weights()
    weight2 = parent2.model.get_weights()
    
    new_weight1 = weight1
    new_weight2 = weight2
    
    gene = random.randint(0, len(weight1)-1)
    
    new_weight1[gene] = weight2[gene]
    new_weight2[gene] = weight1[gene]
    
    return np.asarray([new_weight1, new_weight2])
    


