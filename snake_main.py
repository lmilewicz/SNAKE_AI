# -*- coding: utf-8 -*-

from random import randint
import numpy as np
import time
import sys

from snake_game import SnakeGame
from snake_nn import (SnakeNetwork, model_crossover)

def printProgress(name, i, n, start):
    sys.stdout.write('\r%s Progress: %0.2f percent. Execution time: %0.2f' % (name, 100*(i+1)/n, time.time() - start))
    sys.stdout.flush()
    
def generateNewPopulation(n):
    snakesPopulation = []
    start = time.time()
    for i in range(n):
        snakesPopulation.append(SnakeNetwork())
        printProgress("generateNewPopulation", i, n, start)
    print("\n")
    return snakesPopulation

def playGame(z, n, snakesPopulation):
    scoreArray = np.zeros(n)
    start = time.time()
    for i, snake in enumerate(snakesPopulation): 
        game = SnakeGame()
        x = game.start()
        score = -999
        for j in range(400):
            [x, score] = game.step(snake.predict_action(x))
            if score >= 0: 
                break
        scoreArray[i] = score*100 + j
        
        printProgress("Snake game", i, len(snakesPopulation), start)
    print("\nBest score for generation %d: %d. Time: %0.2f\n" %  (z, np.max(scoreArray), time.time() - start))
    
    return scoreArray

if __name__ == "__main__":
    n = 20
    parent1 = SnakeNetwork()
    score = 0
    snakesPopulation = generateNewPopulation(n)
    #while score < 2:
    #    snakesPopulation = generateNewPopulation(n)
    #    scoreArray = playGame(-1, n, snakesPopulation)
    #    score = np.max(scoreArray)
    
    for z in range(1000):
        scoreArray = playGame(z, n, snakesPopulation)
        if np.max(scoreArray) <= 0:
            print("Snake population from scratch")
            snakesPopulation = generateNewPopulation(n)
        else:
            parent1 = snakesPopulation[np.argmax(scoreArray)]
            scoreArray[np.argmax(scoreArray)] = -1
            if np.max(scoreArray) > 0:
                parent2 = snakesPopulation[np.argmax(scoreArray)]
            else:
                parent2 = snakesPopulation[randint(0, len(snakesPopulation)-1)]                
            for child in snakesPopulation:
                child.model.set_weights(model_crossover(parent1, parent2)[randint(0, 1)])
                child.model.set_weights(child.model_mutate(child.model.get_weights()))

        #game = SnakeGame(gui = True)
        #x = game.start()
        #for j in range(100):
        #    [x, score] = game.step(parent1.predict_action(x))
        #    if score >= 0: 
        #        break
