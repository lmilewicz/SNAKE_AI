# parent1 = snakes_population[np.argmax(fitness_array)]
# fitness_array[np.argmax(fitness_array)] = -1
# if np.max(fitness_array) > 0:
#     parent2 = snakes_population[np.argmax(fitness_array)]
# else:
#     parent2 = snakes_population[randint(0, len(snakes_population) - 1)]
# for x, child in enumerate(snakes_population):
#     child.model.set_weights(model_crossover(parent1, parent2)[randint(0, 1)])
#     child.model.set_weights(model_mutate(child.model.get_weights()))


# sys.stdout.write("\rBest score for gen %d: %d. Fitness: %d. Median: %d. Progress: %0.2f. Time: %0.2f. "
#                  "FitArr: %s.          " %
#                  (z, best_score, np.max(fitness_array), np.median(fitness_array), 100 * (z + 1) / total_generations,
#                   time.time() - start, ", ".join(str(int(x)) for x in array_to_print)))
# sys.stdout.flush()

# snake_game.py

# def input_coordinates(self):
#     x = [self.snake[0][0] / self.board["height"], self.snake[0][1] / self.board["width"],
#          (self.board["height"] - self.snake[0][0]) / self.board["height"],
#          (self.board["width"] - self.snake[0][1]) / self.board["width"],
#          (self.food[0] - self.snake[0][0]) / self.board["height"],
#          (self.food[1] - self.snake[0][1]) / self.board["width"],
#          (self.snake[len(self.snake) - 1][0] - self.snake[0][0]) / self.board["height"],
#          (self.snake[len(self.snake) - 1][1] - self.snake[0][1]) / self.board["width"],
#          (self.snake[int(len(self.snake) / 2)][0] - self.snake[0][0]) / self.board["height"],
#          (self.snake[int(len(self.snake) / 2)][1] - self.snake[0][1]) / self.board["width"]]
#     x = np.array(x)
#     return x.reshape(1, 10)

# def step(self, key):
#     # 0 - UP
#     # 1 - RIGHT
#     # 2 - DOWN
#     # 3 - LEFT
#     if self.done: return self.end_game()
#     self.create_new_point(key)
#     if self.food_eaten():
#         self.score += 1
#         self.generate_food()
#     else:
#         self.remove_last_point()
#         self.check_collisions()
#     if self.gui: self.render()
#     # return self.generate_observations()
#     return [self.input_coordinates(), -1]
#
# def create_new_point(self, key):
#     new_point = [self.snake[0][0], self.snake[0][1]]
#     if key == 0:
#         new_point[0] -= 1
#     elif key == 1:
#         new_point[1] += 1
#     elif key == 2:
#         new_point[0] += 1
#     elif key == 3:
#         new_point[1] -= 1
#     self.snake.insert(0, new_point)


# def generate_observations(self):
#    return self.done, self.score, self.snake, self.food