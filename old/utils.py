# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 23:31:02 2019

@author: lukas
"""

load_saved_pool = False
save_current_pool = True
current_pool = []
fitness = []
total_models = 50

generation = 1

highest_fitness = -1
best_weights = []


def save_pool():
    for xi in range(total_models):
        current_pool[xi].save_weights("SavedModels/model_new" + str(xi) + ".keras")
    print("Saved current pool!")


def showGameOverScreen(crashInfo):
    # Perform genetic updates here

    global current_pool
    global fitness
    global generation
    new_weights = []
    total_fitness = 0

    # START ADD
    global highest_fitness
    global best_weights
    updated = False
    # END ADD

    # Adding up fitness of all birds
    for select in range(total_models):
        total_fitness += fitness[select]
        # START ADD
        if fitness[select] >= highest_fitness:
            updated = True
            highest_fitness = fitness[select]
            best_weights = current_pool[select].get_weights()
        # END ADD

    # REMOVE HERE


    # ADD HERE
    # Get top two parents
    parent1 = random.randint(0,total_models-1)
    parent2 = random.randint(0,total_models-1)

    for i in range(total_models):
        if fitness[i] >= fitness[parent1]:
            parent1 = i

    for j in range(total_models):
        if j != parent1:
            if fitness[j] >= fitness[parent2]:
                parent2 = j


    for select in range(total_models // 2):
        cross_over_weights = model_crossover(parent1, parent2)
        if updated == False:
            cross_over_weights[1] = best_weights
        mutated1 = model_mutate(cross_over_weights[0])
        mutated2 = model_mutate(cross_over_weights[1])
        new_weights.append(mutated1)
        new_weights.append(mutated2)

    # Reset fitness scores for new round
    # Set new generation weights
    for select in range(len(new_weights)):
        fitness[select] = -100
        current_pool[select].set_weights(new_weights[select])
    if save_current_pool == 1:
        save_pool()

    generation += 1
    return


def main():
    # Initialize all models
    for i in range(total_models):
        model = create_model()
        current_pool.append(model)
        # reset fitness score
        fitness.append(-100)
    
    if load_saved_pool:
        for i in range(total_models):
            current_pool[i].load_weights("SavedModels/model_new"+str(i)+".keras")

if __name__ == '__main__':
    main()