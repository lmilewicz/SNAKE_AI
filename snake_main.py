# -*- coding: utf-8 -*-

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
    best_score = 0
    for i, snake in enumerate(snakes_population):
        game = SnakeGame()
        x = game.start()
        prev_score = score = 0
        prev_j = 0
        for j in range((score+1)*100):
            [x, score, end] = game.step(snake.predict_action(x))
            if score > prev_score:
                prev_score = score
                prev_j = j
            if end > 0 or j - (score+1)*50 > prev_j:
                if end == 0: game.end_game()
                break
        if score > best_score:
            best_score = score
        fitness_array[i] = calculate_fitness(score, j)
        snake.set_fitness(fitness_array[i])
        # print_progress("Snake game", i, len(snakes_population), start)
    return [fitness_array, best_score]


def run_generations(n, generations, model_filename, elite_size):
    snakes_population = generate_new_population(n)
    start = time.time()

    for z in range(generations):
        [fitness_array, best_score] = play_game(z, n, snakes_population)
        print_total_progress(z, best_score, fitness_array, generations, start)
        snakes_population = next_generation(snakes_population, int(n*elite_size)+1)

    best_snake = elitism_selection(snakes_population, 1)[0]
    save_model(best_snake.model, model_filename)


def main(n, generations, load_and_play, model_filename, elite_size):
    if load_and_play == 0:
        run_generations(n, generations, model_filename, elite_size)
    else:
        parent = SnakeNetwork()
        parent.model = load_saved_model(model_filename)
        game = SnakeGame(gui=True)
        x = game.start()
        prev_score = score = 0
        prev_j = 0
        x_array = []
        x1_array = []
        end = 0
        for j in range(400):
            [x, score, end] = game.step(parent.predict_action(x))
            if score > prev_score:
                prev_score = score
                prev_j = j
            if end > 0 or j - 100 > prev_j:
                break
            x_array.append(x)
            x1_array.append(parent.model.predict(x))
        if end == 0: game.end_game()
        print(x_array)
        print(x1_array)


if __name__ == "__main__":
    n = 20
    generations = 500
    load_and_play = 0
    model_filename = "model"
    elite_size = 0.1

    if len(sys.argv) > 0:
        n = int(sys.argv[1])
        if len(sys.argv) > 1:
            generations = int(sys.argv[2])
            if len(sys.argv) > 2:
                load_and_play = int(sys.argv[3])
                if len(sys.argv) > 3:
                    model_filename = str(sys.argv[4])
                    if len(sys.argv) > 4:
                        elite_size = float(sys.argv[5])
    main(n, generations, load_and_play, model_filename, elite_size)
