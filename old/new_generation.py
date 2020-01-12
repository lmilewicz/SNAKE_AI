# -*- coding: utf-8 -*-

from old.selection import *

class NewGeneration:
    def __init__(self):
        self.num_parents = 2

    def next_generation(self, snakes_population):

        snakes_population = elitism_selection(snakes_population, self.num_parents)
        random.shuffle(snakes_population)

        next_generation = []

        # Decrement lifespan
        for snake in snakes_population:
            snake.lifespan -= 1

        for snake in snakes_population:
            # params = individual.network.params
            # board_size = individual.board_size
            # hidden_layer_architecture = individual.hidden_layer_architecture
            # hidden_activation = individual.hidden_activation
            # output_activation = individual.output_activation
            lifespan = snake.lifespan

            # If the individual is still alive, they survive
            if lifespan > 0:
                next_generation.append(snake)

        while len(next_generation) < len(snakes_population):
            p1, p2 = roulette_wheel_selection(snakes_population, 2)

            c1, c2 = self._crossover(p1_W_l, p2_W_l, p1_b_l, p2_b_l)
            self._mutation(c1, c2)

            ### ADD mutation

            # Create children from chromosomes generated above
            c1 = Snake(p1.board_size, chromosome=c1_params, hidden_layer_architecture=p1.hidden_layer_architecture,
                       hidden_activation=p1.hidden_activation, output_activation=p1.output_activation,
                       lifespan=self.settings['lifespan'])
            c2 = Snake(p2.board_size, chromosome=c2_params, hidden_layer_architecture=p2.hidden_layer_architecture,
                       hidden_activation=p2.hidden_activation, output_activation=p2.output_activation,
                       lifespan=self.settings['lifespan'])

            # Add children to the next generation
            next_pop.extend([c1, c2])

        # Set the next generation
        random.shuffle(next_generation)
        return next_generation


    def crossover(self, parent1_weights, parent2_weights)
        child1_weights, child2_weights = None, None
        child1_bias, child2_bias = None, None

        child1_weights, child2_weights = single_point_binary_crossover(parent1_weights, parent2_weights,

        return child1_weights, child2_weights


    def _mutation(self, child1_weights: np.ndarray, child2_weights: np.ndarray,
                  child1_bias: np.ndarray, child2_bias: np.ndarray) -> None:
        scale = .2
        rand_mutation = random.random()
        mutation_bucket = np.digitize(rand_mutation, self._mutation_bins)

        mutation_rate = self._mutation_rate
        if self.settings['mutation_rate_type'].lower() == 'decaying':
            mutation_rate = mutation_rate / sqrt(self.current_generation + 1)

        # Gaussian
        if mutation_bucket == 0:
            # Mutate weights
            gaussian_mutation(child1_weights, mutation_rate, scale=scale)
            gaussian_mutation(child2_weights, mutation_rate, scale=scale)

            # Mutate bias
            gaussian_mutation(child1_bias, mutation_rate, scale=scale)
            gaussian_mutation(child2_bias, mutation_rate, scale=scale)

        # Uniform random
        elif mutation_bucket == 1:
            # Mutate weights
            random_uniform_mutation(child1_weights, mutation_rate, -1, 1)
            random_uniform_mutation(child2_weights, mutation_rate, -1, 1)

            # Mutate bias
            random_uniform_mutation(child1_bias, mutation_rate, -1, 1)
            random_uniform_mutation(child2_bias, mutation_rate, -1, 1)

        else:
            raise Exception('Unable to determine valid mutation based off probabilities.')